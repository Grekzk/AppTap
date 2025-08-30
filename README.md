# AppTap: Streamline Your Fresh Windows Setup 

Reinstalling Windows can be a pain. You get the core system up and running, but then comes the time-consuming task of installing all your essential applications. AppTap takes the hassle out of this process, letting you get back to what you love, faster.

# How Does AppTap Work?

Personalized Selection: AppTap presents you with a list of applications chosen by you.

Customization is Key: The choice is yours. Select only the applications you want and skip the rest. AppTap lets you create a personalized Windows environment that reflects your needs and preferences.

Quick and Efficient Installation: Gone are the days of surfing through endless websites with your essential apps. AppTap automates this process, saving you precious time and frustration.

# Benefits of Using AppTap

Save Time: Get back to gaming, working, or socializing on your freshly installed Windows system in no time. AppTap eliminates the tedious task of manual application installation.

Simplified Setup: AppTap provides a user-friendly interface that makes setting up your new Windows environment a breeze, even for non-technical users.

Peace of Mind: Rest assured that AppTap is installing applications only from sources you provided.

# Who is AppTap For?

AppTap is perfect for anyone who wants to streamline their Windows setup process. Whether you're a tech-savvy gamer, a busy professional, or a student setting up a new computer, AppTap saves you valuable time and effort.

Download AppTap today and experience a faster, smoother, and more personalized Windows installation!

# Installation

If you've got python on your device: all of the necessary files are available at master branch.

If you want a packaged program (.exe): download AppTap.zip, located at exe branch. Check WARNINGS.

If you want to package it yourself: master branch + (pyinstaller --noconfirm --onedir --windowed --icon "path\to\Data\logo.ico" --add-data "path\to\Data;Data/" --paths "path\to\\.venv\Lib\site-packages"  "path\to\AppTap.py").

*After packaging don't forget to cut "Data" folder from "_internal" and paste it to "AppTap.exe" location. Check WARNINGS.

# WARNINGS

As AppTap is using user provided download links and runs them, windows defender recognizes it as a virus.
Explanation: AppTap doesn't check user's links, so they could be dangerous, all responsibility lies on user.

To work properly AppTap requires to be launched as administrator.

AppTap is offline program, so that it saves your links locally (by default in "Data").

# Community

If you have the ideas how to imrove AppTap, have some issues or want to discuss it, I'll be grateful to know about this or help you in any way.


