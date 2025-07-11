# pylint: skip-file

from blockbuster_oop import Video, Customer, VideoStore, VendingMachine, DVD, Rental
import pytest


@pytest.fixture
def matrix() -> Video:
    return Video("The Matrix", 1999, 150)


@pytest.fixture
def Spy() -> Video:
    return Video("Spy", 2010, 150)


@pytest.fixture
def Cyber() -> DVD:
    return DVD("Cyber", 2010, 150)

# customer pytest fixtures


@pytest.fixture
def gem() -> Customer:
    return Customer("Gem", "Lo", "05/05/2003")


@pytest.fixture
def john() -> Customer:
    return Customer("John", "Smith", "24/01/1980")


@pytest.fixture
def mike() -> Customer:
    return Customer("Mike", "Lane", "24/01/1981")


def test_customer_name(john):
    assert john.get_name() == "John Smith"


def test_video_invalid_title():
    """Raises an exception if title is not a string"""
    with pytest.raises(Exception):
        Video(3, 2010, 150) == "Please enter a valid title"


def test_video_empty_title():
    """Raises an exception if title is empty"""
    with pytest.raises(Exception):
        Video("", 2010, 150) == "Please enter a valid title"

# valid year?


def test_video_invalid_year():
    """Raises an exception if year is not a valid year"""
    with pytest.raises(Exception):
        Video("Spy", "hi", 150) == "Please enter a valid year"


def test_video_year_too_far_in_future():
    """Raises an exception if year is in the future"""
    with pytest.raises(Exception):
        Video("Spy", 5000, 150) == "Year is too far into the future"


def test_video_invalid_runtime():
    """Raises an exception if runtime is not an integer"""
    with pytest.raises(Exception):
        Video("Spy", 2010, "l") == "Please enter a valid runtime"


def test_video_invalid_negative_runtime():
    """Raises an exception if runtime is a negative integer"""

    with pytest.raises(Exception):
        Video("Spy", 2010, -10) == "Runtime cannot be negative"


def test_video_runtime_too_long():
    """Raises an exception if runtime is longer than 24 hours(1440 minutes)"""

    with pytest.raises(Exception):
        Video("Spy", 2010, 1500) == "Runtime is too long"


def test_video_runtime_too_short():
    """Raises an exception if runtime is shorter than 10 minutes"""

    with pytest.raises(Exception):
        Video("Spy", 2010, 5) == "Runtime is too short"


def test_customer_invalid_first_name():
    """Raises an exception if first name is invalid"""
    with pytest.raises(Exception):
        Customer(5, "Smith", "24/01/1980") == "Please enter a valid first name"


def test_customer_empty_first_name():
    """Raises an exception if first name is empty"""
    with pytest.raises(Exception):
        Customer("", "Smith", "24/01/1980") == "Cannot leave it empty"


def test_customer_invalid_last_name():
    """Raises an exception if last name is invalid"""
    with pytest.raises(Exception):
        Customer("John", 5, "24/01/1980") == "Please enter a valid first name"


def test_customer_empty_last_name():
    """Raises an exception if last name is empty"""
    with pytest.raises(Exception):
        Customer("John", "", "24/01/1980") == "Cannot leave it empty"


def test_customer_invalid_date_of_birth():
    """Raises an exception if date of birth is invalid"""
    with pytest.raises(Exception):
        Customer("John", "Smith", 1980) == "Please enter a valid first name"


def test_customer_empty_date_of_birth():
    """Raises an exception if date of birth is empty"""
    with pytest.raises(Exception):
        Customer("John", "Smith", "") == "Cannot leave it empty"


def test_gets_customer_full_name(gem):
    """Gets customer's first and last name and returns the full name"""
    assert gem.get_name() == "Gem Lo"


def test_gets_customer_age(mike):
    """Gets customer's date of birth and calculates their age"""
    assert mike.age() == 43

# Another test for if month and date is higher than current month and date


def test_gets_customer_younger_than_13():
    "Raises an exception if customer is younger than 13"

    with pytest.raises(Exception):
        Customer("Maggie", "Holt", 2017) == "You have to be 13+"


"""Tests for VideoStore class"""

# def tests_more_than_10_films():


def tests_empty_store():
    with pytest.raises(Exception):
        VideoStore([])


def test_find_video_by_title(matrix):

    store = VideoStore([matrix])

    assert store.find_video_by_title(
        "The Matrix") == matrix


def test_find_video_by_title_invalid(matrix):
    store = VideoStore([matrix])

    with pytest.raises(Exception):
        store.find_video_by_title(
            "Batman") == "Non-existent Movie"


def test_video_is_available(matrix):
    store = VideoStore([matrix])

    assert store.is_available("The Matrix") == True


# def test_video_not_available():
#     matrix = Video("The Matrix", 1999, 150)
#     store = VideoStore([matrix])
#     rent_video ...
#     assert store.is_available("The Matrix") == False


def test_outstanding_fine_zero(john):
    assert john.outstanding_fine == 0


def test_pay_off_outstanding_fine():
    lola = Customer("Lola", "Los", "15/11/1996")
    lola.outstanding_fine += 6000
    lola.pay_off_fine(6000)
    assert lola.outstanding_fine == 0


def test_pay_off_some_outstanding_fine():
    lola = Customer("Lola", "Los", "15/11/1996")
    lola.outstanding_fine += 6000
    lola.pay_off_fine(4000)
    assert lola.outstanding_fine == 2000


def test_rent_video_valid(matrix, john):
    store = VideoStore([matrix])

    assert isinstance(store.rent_video("The Matrix", john), Rental)


def test_rent_video_fine_over_5000():
    matrix = Video("The Matrix", 1999, 150)
    store = VideoStore([matrix])
    marcus = Customer("Marcus", "Long", "23/09/1988")
    marcus.outstanding_fine += 5500

    with pytest.raises(Exception):
        store.rent_video(
            "The Matrix", marcus) == "Cannot rent videos - outstanding fines too high"


def test_rent_video_return_video_early(matrix, john):
    """Tests renting and returning a video before due date"""

    store = VideoStore([matrix])

    rental1 = store.rent_video("The Matrix", john)

    store.return_video(rental1, "15/09/2024")
    assert john.outstanding_fine == 0


def test_rent_video_return_video_late(matrix, john):
    """Tests renting and returning a video after due date which incurs a fine"""

    store = VideoStore([matrix])

    rental1 = store.rent_video("The Matrix", john)

    store.return_video(rental1, "15/10/2024")
    assert john.outstanding_fine == 1000


def test_rent_video_return_video_late_same_release_year():
    """Tests renting and returning a video after due date and film released this year"""
    paramount = Video("Paramount", 2024, 150)
    store = VideoStore([paramount])
    holly = Customer("Holly", "Flannagan", "25/05/2000")

    rental2 = store.rent_video("Paramount", holly)

    store.return_video(rental2, "16/11/2024")
    assert holly.outstanding_fine == 1500


def test_return_rewounded_video_valid(john):

    store = VideoStore([
        Video('The Matrix', 1999, 150),
        Video('The Terminator', 1985, 108)
    ])

    rental = store.rent_video('The Matrix', john)
    video = rental.video

    video.watch()
    video.rewind()
    store.return_video(rental, '01/08/2020')
    assert john.outstanding_fine == 0


def test_rewinding_already_rewounded_video(john):
    """Raises an exception if a rewounded video is rewounded again"""
    store = VideoStore([
        Video('The Matrix', 1999, 150),
        Video('The Terminator', 1985, 108)
    ])

    rental = store.rent_video('The Matrix', john)
    video = rental.video

    video.watch()
    video.rewind()

    with pytest.raises(Exception):
        video.rewind() == "Video is already rewounded"


def test_watching_video_not_rewounded(john):
    """Raises an exception if tries to watch an rewounded video"""
    store = VideoStore([
        Video('The Matrix', 1999, 150),
        Video('The Terminator', 1985, 108)
    ])

    rental = store.rent_video('The Matrix', john)
    video = rental.video

    video.watch()

    with pytest.raises(Exception):
        video.watch() == "Video needs to be rewound first"


def test_returning_unrewounded_video(john):
    """Raises an error if customer returns an unrewounded video"""
    store = VideoStore([
        Video('The Matrix', 1999, 150),
        Video('The Terminator', 1985, 108)
    ])

    rental = store.rent_video('The Matrix', john)
    video = rental.video

    video.watch()

    with pytest.raises(Exception):
        store.return_video(
            rental, '01/08/2020') == "Rewind the video before returning it"


# tests for DVD and Vending machine


def test_DVD_rental_price_valid(Cyber):
    assert Cyber.rental_price() == 1200


def test_watched_DVD_and_returned(Cyber):
    """Rent and watched DVD and can return without rewinding it"""
    store = VendingMachine([Cyber])

    john = Customer('John', 'Smith', '24/01/1980')

    rental = store.rent_video("Cyber", john)
    video = rental.video

    video.watch()
    store.return_video(rental, '01/08/2020')

    assert store.availability[rental.video.title] == True


def test_6_DVD_in_Vending(Cyber):

    with pytest.raises(ValueError, match="A video store can't carry more than 5 videos"):
        VendingMachine([Cyber, Cyber, Cyber, Cyber, Cyber, Cyber])
