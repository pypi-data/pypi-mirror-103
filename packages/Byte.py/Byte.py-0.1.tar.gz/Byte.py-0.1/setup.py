from setuptools import setup, find_packages

setup(
        name='Byte.py',
        version='0.1',
        description='A Python API Wrapper to interact with with the SocialMedia platform Byte.co',
        long_description="""
        # Byte.py
        Byte.py is a python wrapper for the inofficial API that runs the SocialMedia platform Byte.co. 
        # Basic usage
        ```python
        from ByteAPI import ByteAPI

        byteClient = ByteAPI(<Your Token>)
        print(byteClient.username)
        ```
        """,
        long_description_content_type='text/markdown',
        url='https://github.com/RPwnage/Byte.py',
        author='rpwnage',
        author_email='rpwnage@protonmail.com',
        license='MIT',
        packages=find_packages(),
        install_requires=["requests"],
        keywords=['api', 'byte.co', 'byte'],
        zip_safe=False
    )
