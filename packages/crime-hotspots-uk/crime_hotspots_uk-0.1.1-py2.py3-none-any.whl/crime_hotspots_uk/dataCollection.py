"""
This module is used to download and analyse data from the data.police.uk API.
"""

import pandas as pd
from pandas import json_normalize

from tqdm.auto import trange, tqdm

import requests
import json

from datetime import date, timedelta

import seaborn as sns
from matplotlib import pyplot as plt
from textwrap import wrap

from math import sqrt

from shapely.geometry import Polygon, box, MultiPolygon

from crime_hotspots_uk.constants import (
    baseURL,
    crime_categories_url,
    ignore,
)
from crime_hotspots_uk.locations.constituincy import Constituincy


class Reclaim:
    """This class handles all downloading and processing of the data."""

    def __init__(
        self,
        name,
        location_names,
        location_type=Constituincy,
        usage="crime",
    ):
        """This function initiates the class

         It does this by downloading the location boundaries and crime type
         options from the `UK Police API <https://data.police.uk/docs/>`_.

        :param usage: Wether to get crime data or stop and search data from the
            police API. If 'crime' is passed the class will use the `Street
            level crimes <https://data.police.uk/docs/method/crime-street/>`_
            method, if search is passed it will use the `Stop and searches by
            area <https://data.police.uk/docs/method/stops-street/>`_ method.
        :type usage: string, optional

        :raise AssertionError: This error is raised if the string passed to
            usage is not 'crime' or 'search'.
        """

        # Set the file_name member variable to the passed file name
        self.name = name

        # Set the usage member variable depending on the passed usage, this
        # variable is directly used to set the URL and should not be changed
        # If the passed usage is not either 'crime' or 'search' an assertation
        # error is raised
        if usage == "crime":
            self.usage = "crimes-street"
        elif usage == "search":
            self.usage = "stops-street"
        else:
            assert False, 'usage argument should be either "crime" or "search"'

        self.locations = location_type(location_names, name)
        temp = self.locations.locations["shapes"].apply(self.fix_polygons)
        self.locations.locations["shapes"] = temp

        # Update the local list of potential crime types by pulling from
        # https://data.police.uk/docs/method/crime-categories/
        url = crime_categories_url
        payload = {}
        files = {}
        headers = {}
        response = requests.request(
            "GET", url, headers=headers, data=payload, files=files
        )

        # Create a dictionary of the possible crime types and their names
        self.crime_types = {}
        for i in response.json():
            self.crime_types[i["name"]] = i["url"]

    def get_data(self, crime_type):
        """Download data for a specified crime type.

        This is also used to download stop and search data. To do so make sure
        self.usage has been set previously.

        :param crime_type: The crime type to download the data for. It must be
            one of the types listed in self.crime_types, it should be the
            readable name (without any -/_) The full explanation of what each
            category is can be infered from the `Police website <https://www.police.uk/pu/contact-the-police/what-and-how-to-report/what-report/>_` # noqa e501
        :type crime_type: string, required

        :return: Will return true if it managed to successfully download and
            validate the data. If it fails to it will return false.
        :rtype: bool
        """

        # Check if the crime type is valide then set the crime type to a member
        # variable so it can later be used to anotate graphs
        assert crime_type in self.crime_types.keys()
        self.crime_type = crime_type

        # Create a list to hold all the crime data once its downloaded
        crimes = []

        # Loop through all the constituincies
        for area in tqdm(self.locations.locations.index, desc="Areas"):
            for polygon in tqdm(
                self.locations.locations["shapes"][area], desc="Polygons", leave=False
            ):
                # Get the crimes for the current Area
                temp = self.get_crimes(
                    polygon.exterior.coords,
                    self.locations.locations["Constituincy Name"][area],
                )

                # If the data that is retrieved is a dataframe then append it
                # to the list of crime dataframes
                if isinstance(temp, pd.DataFrame):
                    crimes.append(temp)

        # Convert the list of crime dataframes to one big dataframe
        self.all_crimes = pd.concat(crimes)

        # If you have reached here the function was executed successfully
        return True

    def get_crimes(self, coords, constituincy):
        """Download all crimes of a specific type within a boundary

        :param coords: A two deep list containing latitude and longitude
            coordinate pairs
        :type coords: list
        :param constituincy: The name of the constituincy the data is for, this
            name will be appended as a column to the output dataframe to ensure
            that each constituincy can be selected individualy
        :type coords: string

        :return: Returns either a pandas dataframe if the data retireval was
            successfull or NONE if it wasn't
        :rtype: pandas.dataframe
        """

        # Create an empty string that will be used to send the coordinates in
        # the API request
        location = ""

        # Loop through all the coordinate pairs
        for i in range(0, len(coords)):
            # Add each coordinate pair to the API request string
            temp = str(coords[i][1])[0:9] + "," + str(coords[i][0])[0:9] + ":"
            location = location + temp

        # Remove the traling `:` from the request
        location = location[:-1]

        # Set the start and end date fo the request
        start_date = date(2018, 3, 1)  # start date
        end_date = date(2021, 2, 1)  # end date

        # Create a list of dates that can be added to the API request
        dates = (
            pd.date_range(start_date, end_date - timedelta(days=1), freq="MS")
            .strftime("%Y-%m")
            .tolist()
        )

        # Create an empty list to hold the returned JSONS of the crime data
        crime_jsons = []

        # Loop through the list of dates
        for current_date in tqdm(dates, leave=False, desc="Months"):
            # Generate the URL to be sent by using the URL gen function
            url = self.url_gen(location, current_date)

            # No payload or headers are required for the request
            payload = {}
            headers = {}

            # The police API only accepts requests shorter than 4096 characters
            if len(url) > 4096:
                print("url too long")
                return

            # Send the request and save the response
            response = requests.request("GET", url, headers=headers, data=payload)

            # Check to see if the response code was correct (200), if it wasn't
            # print out a warning message and return NONE
            if response.status_code == 404:
                print("-" * 10)
                print("ERROR: response code 404, page not found")
                print("URL was:", url)
                print(
                    "This error probably means a cosntant variable has been spelt incorrectly"  # noqa: E501
                )
                return
            elif response.status_code == 429:
                print("-" * 10)
                print("ERROR: response code 429, too many requests")
                print("URL was:", url)
                print("Doccumentation at: https://data.police.uk/docs/api-call-limits/")
                return
            elif response.status_code == 503:
                print("-" * 10)
                print("ERROR: response code 503, more than 10,000 crimes in area")
                print("URL was:", url)
                print(
                    "Doccumentation at: https://data.police.uk/docs/method/crime-street/"  # noqa: E501
                )
                return
            elif response.status_code == 200:
                # If the response code was 200 add the JSON ro the list of data
                crime_jsons.append(json_normalize(json.loads(response.text)))
            else:
                print("-" * 10)
                print("ERROR: unkown response code")
                print("URL was:", url)
                print("response code: ", response.status_code)
                return

        # Convert the list of data to a dataframe
        crimes = pd.concat(crime_jsons)

        # If data was found ensure the dataframe is formatted correctly, if not
        # return NONE
        if crimes.shape[0] > 0:
            # Set the latitude and longitude to numeric values
            crimes["location.latitude"] = pd.to_numeric(crimes["location.latitude"])
            crimes["location.longitude"] = pd.to_numeric(crimes["location.longitude"])

            # Create a pretty name that is easily readable
            # Example: `On or near Hyde Park Place - Leeds North West`
            crimes["pretty name"] = (
                crimes["location.street.name"] + " - " + str(constituincy)
            )

            # Add a column with the constituincy that the data is from
            crimes["constituincy"] = str(constituincy)
            crimes["Type"] = "Street"

            # Reset the index to number all entries from 0 to length of the data
            crimes.reset_index(inplace=True, drop=True)

            # Return the dataframe of crimes
            return crimes

        # Return NONE if no data was found
        return

    def fix_locations(self):
        """Fix locations in the self.all_crimes dataframe

        This is needed because some of the location names used by the police are
        used for multiple locations. For instance `On or near bus stop` doesn't
        tell us which bus stop it was near. This function takes the provided
        latitude and longitude coordinates and identifies which locale with a
        definitive name in the local constituincy is closest.

        :raise AssertionError: This error is raised if a location name can't be
             correctly mapped to a street because there was no points close
             enough.

        """

        # Create a global list of all possible locations in the UK, this
        # contains the street name, latitude, longitude, constuincy and a
        # pretty name made up of the street name and constituincy. Note that
        # one street can appear in two constituincies
        self.global_locales = self.all_crimes[
            [
                "location.street.name",
                "location.latitude",
                "location.longitude",
                "constituincy",
                "pretty name",
            ]
        ]

        # Create a search term to compare each entry agains, the search term
        # is formed from the known non desriptive values in the ignore constant
        search = "|".join(ignore)

        # Create a truth table mask of which locations names are descriptive
        mask = ~self.global_locales["location.street.name"].str.contains(search)

        # Apply the mask to the locales table and reset the index
        # We now have a list of all the descriptive street names which can
        # be filtered by constituincy
        self.global_locales = self.global_locales[mask]
        self.global_locales.reset_index(inplace=True, drop=True)

        # Duplicate the data dataframe
        modified_crimes = self.all_crimes

        # Get the indexes of the columns of interest
        street_id_loc = modified_crimes.columns.get_loc("location.street.name")
        latitude_id_loc = modified_crimes.columns.get_loc("location.latitude")
        longitude_id_loc = modified_crimes.columns.get_loc("location.longitude")
        constituincy_id_loc = modified_crimes.columns.get_loc("constituincy")
        pretty_id_loc = modified_crimes.columns.get_loc("pretty name")
        type_id_loc = modified_crimes.columns.get_loc("Type")

        # Loop through all the crimes in the dataset
        for i in trange(0, modified_crimes.shape[0]):
            # Copy the current street name into a local variable
            street = modified_crimes.iloc[i][street_id_loc]

            # Loop through all the non descriptive street names
            for x in ignore:
                # If the current street contains a non descriptive name then
                if x in street:

                    # Get the name of the constituincy of the current street
                    constituincy = modified_crimes.iloc[i][constituincy_id_loc]

                    # Create a truth mask of which of the global locales
                    # constituincies match the current constituincy
                    mask = self.global_locales["constituincy"] == constituincy

                    # Create a list off possible locations based on all other
                    # locations in the same constituincy using the mask
                    locales = self.global_locales.loc[mask]

                    # Get the local latitude and logntitude values from the data
                    street_lat = modified_crimes.iloc[i][latitude_id_loc]
                    street_lon = modified_crimes.iloc[i][longitude_id_loc]

                    # Set a really high value for the minimum distance between
                    # points, as the program calculates distances betwen the
                    # street and the possilbe locales this will be updated to
                    # represent what the smallest distance is
                    min_distance = 1000000

                    # Set the index to -1 so we know if no nearby locale was
                    # found
                    min_distance_index = -1

                    # Loop through all possible locales
                    for j in range(0, locales.shape[0]):
                        # Get the latitude and longitude of the current
                        # candidate locale
                        locale_lat = locales.iloc[j][1]
                        locale_lon = locales.iloc[j][2]

                        # Calculate the difference between the current street
                        # and the candidate locale
                        lat_diff = street_lat - locale_lat
                        lon_diff = street_lon - locale_lon

                        # Calculate the difference between the two points
                        # TODO: Change this to the haversine formula
                        distance = sqrt((lat_diff) ** 2 + (lon_diff) ** 2)

                        # If the distance is the smalles so far
                        if distance < min_distance:
                            # Update the minimum distance and the index
                            min_distance = distance
                            min_distance_index = j

                    # Check if no locale closer than 1000000 was found
                    if min_distance_index < 0:
                        print(street)
                        print(x)

                    # Get the name of the new street and create the new pretty
                    # name
                    new_street = locales.iloc[min_distance_index][0]
                    pretty_name = new_street + " - " + constituincy

                    # Set the names in the crimes dataframe to the new names
                    self.all_crimes.iat[i, pretty_id_loc] = pretty_name
                    self.all_crimes.iat[i, street_id_loc] = new_street
                    self.all_crimes.iat[i, type_id_loc] = street

    def hotspots_graph(self, top, location, location_type=["All"]):
        """Draw a bargraph of the rates of assult at the top hotspots

        :param top: how many hotspots to plot, for instance 10 would show the
            top 10 hotspots. IF this is set to none all hotspots will be
            graphed.
        :type top: int
        :param location: Where the title of the graph should
            say the data is from
        :type location: string
        :param location_type: Type of location to make the graph for, must be a
             list of location types, each entry must be either `Street` or
            value in the ignore list in constants.py. You can also pass `All`
            to select all crimes. The default value is `All`
        :type location_type: list (optional)
        """

        # Check if fix locations has been run yet, this graph only produces
        # valid data if the locations have been fixed
        if self.global_locales.empty:
            self.fix_locations()

        # If the value passed to top is none then it means graph all locations
        if top is None:
            top = len(self.all_crimes)

        # Check if the location type input is valid
        for x in location_type:
            assert x == "Street" or x == "All" or (x in ignore)

        # If the location_type was ['All'] set
        if location_type == ["All"]:
            location_type = ignore
            location_type.append("Street")

        search = "|".join(location_type)
        print("List of locations: ", location_type)
        print("Search term: ", search)
        # Create a mask of all the crimes that happened at the
        # given location type
        mask = self.all_crimes["Type"].str.contains(search)

        self.crime_list = self.all_crimes.loc[mask]

        # Create a pandas datafram containing the frequency counts of the top
        # locations
        self.hotspots = self.crime_list["pretty name"].value_counts()[:top]
        self.hotspots = self.hotspots.to_frame()

        # Reset the index and rename the columns
        self.hotspots.reset_index(inplace=True)
        self.hotspots.columns = ["locations", "frequency"]

        # Set the seaborn font scale
        sns.set(font_scale=4)

        # Set it so the number listed in the title is the same as the number of
        # bars on the graph
        top = len(self.hotspots["frequency"])

        # Create a barplot of the hotspots
        fig, ax = plt.subplots(figsize=(40, 40))

        # Create the title of the chart depending on if it is crime or stop and
        # search data
        if self.usage == "crimes-street":
            title = (
                "Number of reported "
                + str(self.crime_type)
                + " crimes in locations within "
                + str(location)
                + " since 2018, top "
                + str(top)
                + " locations"
            )
        else:
            title = (
                "Number of stop and searches at locations within "
                + str(location)
                + " since 2018, top "
                + str(top)
                + " locations"
            )

        # Set the graph title to wrap
        title = "\n".join(wrap(title, 60))
        ax.set_title(title)

        # Add data labels to the bats
        for p in ax.patches:
            height = p.get_height()  # height of each horizontal bar is the same
            width = p.get_width()  # width (average number of passengers)
            # adding text to each bar
            ax.text(
                x=width + 1,  # x-coordinate position of data label
                y=p.get_y() + (height / 2),  # y-coordinate position of data label
                s="{:.0f}".format(width),  # data label, formatted to ignore decimals
                va="center",
            )  # sets vertical alignment (va) to center

        # Set a tight layout
        fig.tight_layout()

        # Save the graph
        fig.savefig("locationFrequency.jpeg")

    # UTILITY FUNCTIONS
    def fishnet(self, geometry, threshold):
        """Divide a shapely geometry into small sections

        .. note:: This function is not currently used and is not doccumented

        """
        bounds = geometry.bounds
        xmin = int(bounds[0] // threshold)
        xmax = int(bounds[2] // threshold)
        ymin = int(bounds[1] // threshold)
        ymax = int(bounds[3] // threshold)
        result = []
        for i in range(xmin, xmax + 1):
            for j in range(ymin, ymax + 1):
                b = box(
                    i * threshold,
                    j * threshold,
                    (i + 1) * threshold,
                    (j + 1) * threshold,
                )
                g = geometry.intersection(b)
                if g.is_empty:
                    continue
                result.append(g)
        return result

    def url_gen(self, location, date):
        """Generate the url for API requests

        :param location: String of Lat/Lon coordinates marking out a boundary
        :type location: String
        :param date: The month to get the data for in format yyyy-mm
        :type: date String
        """

        # Check if the API request if for crimes or stop and search data then
        # assemble the URL
        if self.usage == "crimes-street":
            url = (
                baseURL
                + self.usage
                + "/"
                + self.crime_types[self.crime_type]
                + "?poly="
                + location
                + "&date="
                + str(date)
            )
        else:
            url = baseURL + self.usage + "?poly=" + location + "&date=" + str(date)

        return url

    def fix_polygons(self, polygon):
        if type(polygon) == Polygon:
            polygon = MultiPolygon([polygon])
        return polygon
