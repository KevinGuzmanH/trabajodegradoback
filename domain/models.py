from dataclasses import dataclass

@dataclass
class Movie:
    title: str
    year: str
    duration: str
    genre: str
    director: str
    plot: str
    streaming_platforms: list
