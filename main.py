from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import shelve
import initial
# import Selenium Webdriver functionality, the random library for random answers,
# the time library to pause code, the shelve library to store question data, and initial.py to setup drivers

# runs setup script
initial.check_init()


class Session(webdriver.Chrome):
    """
    Class expansion of Webdriver's Chrome class to add specialised support for Membean.

    Attributes:
        email    (str): The user's email.
        password (str): The user's password.
    """
    def __init__(self, email, password):
        # initialise the Chrome class
        webdriver.Chrome.__init__(self)
        # store email attribute in variable
        self.email = email
        # store password attribute in variable
        self.password = password
        # unused variable that no longer has a purpose which may be used in a later commit
        self.studyQuestionAnswered = False

    def login(self):
        # go to Membean login page
        self.get("http://www.membean.com/login/")
        # wait until page has loaded
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.ID, "user_username")))
        # get input fields for login
        fields = [self.find_element_by_id("user_username"), self.find_element_by_id("user_password")]
        # supply email
        fields[0].send_keys(self.email)
        # supply password
        fields[1].send_keys(self.password)
        # submit
        fields[1].submit()
        # print a success message to the screen
        print("login success")

    def start(self, length=15):
        """
        The method to start a Membean session

        Parameters:
            length (int): The length of the session (do not change).
        """
        # find start button
        start_button = self.find_element_by_id("start-button")
        # click start button
        start_button.click()
        try:
            # wait for page to load
            WebDriverWait(self, 10).until(EC.presence_of_element_located((By.ID, "Proceed")))
            if length == 15:
                # find proceed button
                proceed = self.find_element_by_id("Proceed")
                # click proceed button
                proceed.click()
        except:
            print("entering existing session")
        # print a success message to the screen
        print("session start")

    def update(self, gather=False):
        # checks if conditions are met
        # checks if study question has been answered to prevent multiple clicks
        if self.check_for_element(By.CSS_SELECTOR, ".choice.answer.correct"):
            return 1
        # checks if a question has been answered and then stores the data for that question in a binary file
        elif self.check_for_element(By.CSS_SELECTOR, ".choice.correct"):
            if gather:
                data = shelve.open("./data/dicts.db")
                question = self.find_elements(by=By.CLASS_NAME, value="choice")
                for i in range(len(question)):
                    data[str(i)] = [question[i].id,
                                    question[i].text,
                                    i,
                                    "correct" if self.find_elements(by=By.CSS_SELECTOR, value=".choice.correct")[0].id
                                    == (choice.id for choice in question) else "wrong"]
            return 1
        # checks if a study question is present and answers with complete accuracy
        elif self.check_for_element(By.CSS_SELECTOR, "#choice-section > li.choice.answer"):
            button = self.find_element(by=By.CSS_SELECTOR, value="#choice-section > li.choice.answer")
            try:
                button.click()
            except:
                print("bad identifier, error to be fixed in next commit")
            return 1
        # redundant statement that would prevent multiple clicks on a study question
        elif self.check_for_element(By.CSS_SELECTOR, ".choice.answer.correct"):
            return 1
        # checks if a question is present and uses the answer method to click a random answer
        elif self.check_for_element(By.CLASS_NAME, "choice"):
            self.answer()
            return 1
        # checks if the start-button is present(indicating that the dashboard is open)
        elif self.check_for_element(By.ID, "start-button"):
            return 0
        # takes the place of other conditions such as an unknown question or other error
        else:
            print("no result")
            return 1

    def answer(self):
        try:
            # find the possible answers
            options = self.find_elements_by_class_name("choice")
            # click a random answer
            options[random.randint(0, len(options) - 2)].click()
        except:
            # print an error message to the screen
            print("unsupported question")

    def check_for_element(self, mode, value):
        """
        The method to check if an element or multiple elements exist

        Parameters:
            mode  (str): The selection mode.
            value (str): The value to look for through the selection mode.
        """
        # find element
        element = self.find_elements(by=mode, value=value)
        # checks if element exists
        if len(element) > 0:
            return 1
        else:
            return 0


def main():
    session = Session(raw_input("Enter Email: "), raw_input("Enter Password: "))
    # login to membean
    session.login()
    # wait until dashboard has loaded
    WebDriverWait(session, 10).until(EC.presence_of_element_located((By.ID, "start-button")))
    # enter Membean session
    session.start()
    while True:
        # wait 3 seconds between updates to create a more natural robot and to prevent memory overflow
        time.sleep(3)
        # get session status and updates the session
        # checks if session is still active and breaks if not
        status = session.update(True)
        if not status:
            break
    # quit session and close browser
    session.quit()

# standard runtime statement
if __name__ == "__main__":
    main()
