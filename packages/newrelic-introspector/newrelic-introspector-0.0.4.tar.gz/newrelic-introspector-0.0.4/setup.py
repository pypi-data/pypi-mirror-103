import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def guess_next_version(tag_version):
    version, _, _ = str(tag_version).partition("+")
    version_info = list(map(int, version.split(".")))
    if len(version_info) < 4:
        return version
    version_info[1] += 1
    if version_info[1] % 2:
        version_info[3] = 0
    else:
        version_info[3] += 1
    return ".".join(map(str, version_info))


def next_version(version):
    if version.exact:
        return version.format_with("{tag}")
    else:
        return version.format_next_version(guess_next_version, fmt="{guessed}")


setuptools.setup(
    name="newrelic-introspector",
    version="0.1.0",
    author="New Relic",
    author_email="support@newrelic.com",
    maintainer="New Relic",
    maintainer_email="support@newrelic.com",
    license="Apache-2.0",
    description="New Relic Python Process Introspector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/newrelic/newrelic-introspector-python",
    project_urls={
        "Source": "https://github.com/newrelic/newrelic-introspector-python",
        "Bug Tracker": "https://github.com/newrelic/newrelic-introspector-python/issues",
    },
    use_scm_version={
        "version_scheme": next_version,
        "local_scheme": "no-local-version",
        "git_describe_command": "git describe --dirty --tags --long --match *.*.*",
        "write_to": "src/version.txt",
    },
    setup_requires=["setuptools_scm>=3.2,<4"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Monitoring",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    entry_points={
        "console_scripts": ["newrelic-introspector-python=newrelic_introspector:main"]
    },
    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*",
    zip_safe=False,
)
