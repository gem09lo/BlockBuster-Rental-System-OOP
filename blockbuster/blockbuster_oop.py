"""import"""
from datetime import datetime
from datetime import date
from datetime import timedelta


class Video:
    """Videos have a title, year of release, runtime and rental price"""

    def __init__(self, title: str, year: int, runtime: int):
        if not isinstance(title, str):
            raise TypeError("Please enter a valid title")
        if title is None or title == "":
            raise ValueError("Please enter a valid title")

        if not isinstance(year, int):
            raise TypeError("Please enter a valid year")
        if year < 1900:
            raise ValueError("Videos can't be released before 1900")
        if year > date.today().year:
            raise ValueError("Year shouldn't be in the future")

        if not isinstance(runtime, int):
            raise TypeError("Please enter a valid runtime")
        if runtime < 0:
            raise ValueError("Runtime cannot be negative")
        if runtime > 1440:
            raise ValueError("Runtime is too long")
        if runtime < 10:
            raise ValueError("Runtime is too short")

        self.title = title
        self.year = year
        self.runtime = runtime
        self.is_rewound = True

    def display_title(self) -> str:
        """Displays the video title and year in format - title (year)"""
        return f"{self.title} ({self.year})"

    def rental_price(self) -> int:
        """Calculates the price (in pence) of renting the video"""
        today = date.today()
        this_year = today.year
        factor = 1

        if self.runtime > 240:
            factor = 2
        if self.year == this_year:
            return 1000 * factor
        return 500 * factor

    def display_price(self) -> str:
        """Displays the price as £"""
        price_in_pence = self.rental_price()
        price_in_pounds = price_in_pence/100

        return f"£{price_in_pounds:.2f}"

    def watch(self):
        """Watch video if it's rewounded"""
        if not self.is_rewound:
            raise ValueError("Video needs to be rewound first")
        self.is_rewound = False

    def rewind(self):
        """Rewind video if it's been watched"""
        if self.is_rewound:
            raise ValueError("Video is already rewounded")
        self.is_rewound = True


class Customer:
    """Takes customer's first name, last name and date of birth(age)"""

    def __init__(self, first_name: str, last_name: str, date_of_birth: str) -> None:
        if not isinstance(first_name, str):
            raise TypeError("Please enter a valid first name")
        if not isinstance(last_name, str):
            raise TypeError("Please enter a valid last name")
        if not isinstance(date_of_birth, str):
            raise TypeError("Please enter a valid date of birth")
        if first_name == "" or last_name == "" or date_of_birth == "":
            raise ValueError("Cannot leave it empty")

        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.outstanding_fine = 0

        if self.age() < 13:
            raise ValueError("You have to be 13+")

    def get_name(self) -> str:
        """Returns full name of customer"""
        return f"{self.first_name} {self.last_name}"

    def age(self) -> int:
        """Returns age of customer"""
        current_date = datetime.today()
        date_of_birth = datetime.strptime(self.date_of_birth, "%d/%m/%Y")

        age = current_date.year - date_of_birth.year
        if (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day):
            age += 1
        return age

    def pay_off_fine(self, amount: int):
        """Customer pays off outstanding fine and updates the total outstanding amount"""
        self.outstanding_fine -= amount

# pylint: disable=R0903


class Rental:
    """gives due date of two weeks from when the video was rented"""

    def __init__(self, video: Video, customer: Customer) -> None:
        current_date = datetime.today()
        two_weeks = timedelta(days=14)

        self.due_date = current_date + two_weeks
        self.video = video
        self.customer = customer


class VideoStore:
    """Blockbuster stores collection of Video objects.
        Tracks currently rented videos"""

    def __init__(self, videos: list) -> None:
        if len(videos) <= 0:
            raise ValueError("A video store must carry at least some videos")
        if len(videos) > 10:
            raise ValueError("A video store can't carry more than 10 videos")

        self.videos = videos
        self.availability = {}

        for video in videos:
            self.availability[video.title] = True

    def find_video_by_title(self, video_title: str) -> Video:
        """Method to look up a video by it's title and returns Video object if found"""
        for video in self.videos:
            if video_title == video.title:
                return video
        raise ValueError("Non-existent title")

    def is_available(self, video_title: str) -> bool:
        """Method that checks if a video with the given title is available for rent"""
        return self.availability[video_title] is True

    def rent_video(self, title: str, customer: Customer) -> Rental:
        """Ensure that the video with the title given is set to be not available"""
        if not isinstance(customer, Customer):
            raise TypeError("Invalid customer's name")

        video = self.find_video_by_title(title)

        if customer.outstanding_fine > 5000:
            raise ValueError(
                "Cannot rent videos - outstanding fines too high!")
        if self.is_available(title):
            self.availability[title] = False

        return Rental(video, customer)

    def return_video(self, rental: Rental, return_date: str):
        """Customer returns video and checks if outstanding fines are incurred"""
        if not isinstance(rental, Rental):
            raise ValueError("Invalid Rental")
        if not isinstance(return_date, str):
            raise ValueError("Invalid return date")

        return_date_formatted = datetime.strptime(return_date, '%d/%m/%Y')

        if rental.video.is_rewound is False:
            raise ValueError("Rewind the video before returning it")
        if return_date_formatted < rental.due_date:
            self.availability[rental.video.title] = True

        if return_date_formatted > rental.due_date:
            self.availability[rental.video.title] = True
            if rental.video.year == datetime.now().year:
                rental.customer.outstanding_fine += 1500
            else:
                rental.customer.outstanding_fine += 1000


# pylint: disable = W0612
class DVD(Video):
    """DVDs(new kinds of media) to stock and launch BlockBuster vending machines"""

    def rental_price(self):
        return 1200

    def watch(self):
        pass


class VendingMachine(VideoStore):
    """Stores DVDs and can return DVDs"""

    def __init__(self, videos: list) -> None:
        super().__init__(videos)

        if len(videos) > 5:
            raise ValueError("A video store can't carry more than 5 videos")

    def return_video(self, rental, return_date):
        if not isinstance(rental, Rental):
            raise ValueError("Invalid Rental")
        if not isinstance(return_date, str):
            raise ValueError("Invalid return date")

        self.availability[rental.video.title] = True
