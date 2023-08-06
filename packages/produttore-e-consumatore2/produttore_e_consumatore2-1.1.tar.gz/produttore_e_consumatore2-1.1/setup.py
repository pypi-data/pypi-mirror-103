from setuptools import setup, find_packages
from requests import get

gh_api = "https://api.github.com/repos/CastellaniDavide/produttore_e_consumatore2"
gh_raw = "https://raw.githubusercontent.com/CastellaniDavide/produttore_e_consumatore2"

setup(
    name='produttore_e_consumatore2',
    # Lastest release
    version=get(f"{gh_api}/tags").json()[0]['name'].replace("v", ""),
    description=get(gh_api).json()['description'],
    long_description=get(f"{gh_raw}/main/docs/README.md").text,
    long_description_content_type="text/markdown",
    url=get(gh_api).json()['html_url'],
    author=get(gh_api).json()['owner']['login'],
    author_email=get(
        f"https://api.github.com/users/"
        f"{get(f'{gh_api}').json()['owner']['login']}").json()['email'],
    license='GNU',
    packages=find_packages(),
    python_requires=">=3.6",
    platforms="linux_distibution",
    install_requires=[
        i
        for i in get(f"{gh_raw}/main/requirements/requirements.txt").text.split(
            "\n") if "#" not in i and i != ''],
    zip_safe=True
)
