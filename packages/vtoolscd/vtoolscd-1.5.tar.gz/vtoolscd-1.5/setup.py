from setuptools import setup, find_packages
from requests import get

github_api_link = "https://api.github.com/repos/CastellaniDavide/vtools"
github_raw_link = "https://raw.githubusercontent.com/CastellaniDavide/vtools"

setup(
    name='vtoolscd',
    # Lastest release
    version=get(f"{github_api_link}/tags").json()[0]['name'].replace("v", ""),
    description=get(github_api_link).json()['description'],
    long_description=get(f"{github_raw_link}/main/docs/README.md").text,
    long_description_content_type="text/markdown",
    url=get(github_api_link).json()['html_url'],
    author=get(github_api_link).json()['owner']['login'],
    author_email=get(
        f"https://api.github.com/users/"
        f"{get(f'{github_api_link}').json()['owner']['login']}"
    ).json()['email'],
    license='GNU',
    packages=find_packages(),
    python_requires=">=3.6",
    platforms="linux_distibution",
    install_requires=[
        i
        for i in get(
            f"{github_raw_link}/main/requirements/requirements.txt"
        ).text.split("\n") if "#" not in i and i != ''],
    zip_safe=True
)
