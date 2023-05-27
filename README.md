# Waveshare e-Ink Display Info Widgets for Raspberry Pi

This project is a modular system of widgets that can be displayed using an anchor point (top-left) and a custom height and width. The widgets are meant to adapt to the supplied height and width (WIP).

There are currently functional news (headlines from NYT) and weather ([OpenWeather API](https://openweathermap.org/api) free tier), with plans for Google Calendar API integration to show upcoming events.

I am using a Raspberry Pi with Waveshare's 800x480 7.5" B model (Red, Black, and White), but using the script for your model on [Waveshare's Repo](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd) and adding it to `lib`, as well as changing the assignment of `epd` in `main.py` should make it work. If you have a single-color model, you will need to remove the second argument of `epd.display()` in `main.py` at a minimum, and by changing `colorChannels["red"]` to draw to `Limage` rather than `Limage_Other` at declaration, all red will become black instead.