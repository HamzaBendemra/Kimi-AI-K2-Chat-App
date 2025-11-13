from setuptools import setup, find_packages

setup(
    name="kimi-chat-app",
    version="1.0.0",
    description="A Streamlit app for chatting with Kimi AI",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)