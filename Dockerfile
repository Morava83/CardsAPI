ARG PORT=443

FROM cypress/browsers:latest

RUN apt-get update && apt-get install -y python3 python3-pip curl unzip libglib2.0-0 libnss3 libx11-6 libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libappindicator1 libdbus-1-3 libfontconfig1 libpango-1.0-0 libcairo2 libatk1.0-0 libgtk-3-0 libgbm1

COPY requirements.txt .

ENV PATH /home/root/.local/bin:${PATH}

RUN pip install -r requirements.txt

# Install Chrome
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

# Install ChromeDriver
RUN CHROMEDRIVER_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip &&\
    echo "Installing chromium webdriver from ${CHROMEDRIVER_URL}" &&\
    curl -sSL ${CHROMEDRIVER_URL} -o chromedriver_linux64.zip &&\
    unzip -o chromedriver_linux64.zip -d /usr/bin/ &&\
    mv /usr/bin/chromedriver-linux64/chromedriver /usr/bin/ &&\
    rm -rf /usr/bin/chromedriver-linux64/ &&\
    rm chromedriver_linux64.zip

# Check the contents of /usr/bin/
RUN ls -la /usr/bin/

# Check the contents of /usr/bin/chromedriver
RUN ls -la /usr/bin/chromedriver

# Set executable permissions
RUN chmod +x /usr/bin/chromedriver

# Check the contents of /usr/bin/ again
RUN ls -la /usr/bin/

# Check the contents of /usr/bin/chromedriver again
RUN ls -la /usr/bin/chromedriver

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port $PORT
