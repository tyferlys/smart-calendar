from typing import List

from sqlalchemy import String, Date, DateTime, Integer, ForeignKey, Boolean, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.configDataBase import Base


class Day(Base):
    __tablename__ = "tday"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(Date, unique=True)
    status: Mapped[str] = mapped_column(String(60))
    begin_time: Mapped[Time] = mapped_column(Time(timezone=True))
    end_time: Mapped[Time] = mapped_column(Time(timezone=True))

    events: Mapped[List["Event"]] = relationship(back_populates="day")

    def __repr__(self) -> str:
        return (f"Day: id - {self.id}, date - {self.date}, status - {self.status},"
                f" begin time - {self.begin_time}, end time - {self.end_time}")


class Service(Base):
    __tablename__ = "tservice"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(60))
    cost: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    after_pause: Mapped[int] = mapped_column(Integer)

    events: Mapped[List["Event"]] = relationship(back_populates="service")

    def __repr__(self) -> str:
        return (f"Service: id={self.id}, title={self.title}, cost={self.cost}, "
                f"duration={self.duration}, after_pause={self.after_pause}")


class Client(Base):
    __tablename__ = "tclient"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(60))
    first_name: Mapped[str] = mapped_column(String(60))
    middle_name: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str] = mapped_column(String(60), unique=True)
    username: Mapped[str] = mapped_column(String(60), nullable=True)
    telegram_id: Mapped[str] = mapped_column(String(60), nullable=True)

    events: Mapped[List["Event"]] = relationship(back_populates="client")
    reports: Mapped[List["Report"]] = relationship(back_populates="client")
    options: Mapped[List["OptionsClient"]] = relationship(back_populates="client")

    def __repr__(self) -> str:
        return (f"Client: id - {self.id}, last_name - {self.last_name}, "
                f"first_name - {self.first_name}, middle_name - {self.middle_name}, phone - {self.phone}, username - {self.username}, telegram_id - {self.telegram_id}")


class Event(Base):
    __tablename__ = "tevent"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_day: Mapped[int] = mapped_column(Integer, ForeignKey("tday.id"))
    id_service: Mapped[int] = mapped_column(Integer, ForeignKey("tservice.id"))
    id_client: Mapped[int] = mapped_column(Integer, ForeignKey("tclient.id"))
    status: Mapped[str] = mapped_column(String(60))
    time: Mapped[DateTime] = mapped_column(Time(timezone=True))

    day: Mapped["Day"] = relationship(back_populates="events")
    service: Mapped["Service"] = relationship(back_populates="events")
    client: Mapped["Client"] = relationship(back_populates="events")

    def __repr__(self):
        return (f"Event: id - {self.id}, id_day: {self.id_day}, id_service: {self.id_service}, "
                f"id_client: {self.id_client}, self.status: {self.status}, time: {self.time}")


class Owner(Base):
    __tablename__ = "towner"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(60))
    first_name: Mapped[str] = mapped_column(String(60))
    middle_name: Mapped[str] = mapped_column(String(60))
    phone: Mapped[str] = mapped_column(String(60), unique=True)
    password: Mapped[str] = mapped_column(String(60))
    token: Mapped[str] = mapped_column(String(60), nullable=True)

    def __repr__(self) -> str:
        return (f"Owner: id - {self.id}, last_name - {self.last_name}, "
                f"first_name - {self.first_name}, middle_name - {self.middle_name}, phone - {self.phone}, password - {self.password}, token - {self.token}")


class Options(Base):
    __tablename__ = "toptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    begin_time: Mapped[Time] = mapped_column(Time(timezone=True))
    end_time: Mapped[Time] = mapped_column(Time(timezone=True))

    def __repr__(self) -> str:
        return f"Options: id - {self.id}, begin_time - {self.begin_time}, end_time - {self.end_time}"


class Report(Base):
    __tablename__ = "treports"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_client: Mapped[int] = mapped_column(Integer, ForeignKey("tclient.id"))
    text: Mapped[str] = mapped_column(String(60), nullable=True)

    client: Mapped["Client"] = relationship(back_populates="reports")

    def __repr__(self) -> str:
        return f"Report: id - {self.id}, id_client - {self.id_client}, text - {self.text}"


class OptionsClient(Base):
    __tablename__ = "toptions_client"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_client: Mapped[int] = mapped_column(Integer, ForeignKey("tclient.id"))
    is_notification: Mapped[bool] = mapped_column(Boolean)

    client: Mapped["Client"] = relationship(back_populates="options")

    def __repr__(self) -> str:
        return f"OptionsClient: id - {self.id}, id_client - {self.id_client}, is_notification - {self.text}"