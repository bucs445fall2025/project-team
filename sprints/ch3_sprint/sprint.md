# **Project Overview**

## **Application Vision/Goal:**
[Describe the overall purpose and vision of the application. What problem does it solve? Who is the target audience?]
- Purpose/Vision: To predict stock movements over time using multiple models
- Problem: Predicting the stock market is difficult, let's use years of data to do it for us.
- Target Audience: People that don't know too much about the stock market but want to make some smart investments

## **Scope:**
[List the major features and functionalities that define the scope of the project. Keep this high-level to avoid feature creep.]
- GUI showing our stock predictions vs. the real world
- At least one working stock prediction model

## **Deliverables:**
[List what will be delivered by the end of the project, such as a working MVP (Minimum Viable Product), specific features, documentation, etc.]
- Either a website or application to display our predictions
- Performance analysis of our predictions
- User documentation on how to safely invest using our tools

## **Success Criteria:**
[Define what will make this project successful. Examples include meeting deadlines, delivering core functionality, or achieving performance benchmarks.]
- This project will be successful if our model(s) can outperform the S&P 500

## **Assumptions:**
[List any assumptions about the technology, users, or resources that could impact development.]
- N/A at this time

## **Risks:**
[Identify potential risks and challenges, such as technical limitations, resource constraints, or dependency issues.]
- There may be resource limitations in reading and analyzing all the stock data we will need to train our models -- we may not have the compute power to do this in a reasonable amount of time 

## **Design / Architectural Review:**
[Outline the initial thoughts on application architecture. Will it be monolithic or microservices? Will it use a database? What major components will be included?]
- Monolithic
- Will use a database to store our predictions to model against the real world
- May use a home server for hosting/training the models
- Major components N/A at this time

## **Test Environment:**
[Define how the application will be tested. Will you use automated tests? What environment will the tests run in?]
- The application will be tested using a development environment with automated and manual testing

---

# **Team Setup**

## **Team Members:**
- Brendon Paolino
- Michael Zheng
- Gavin Suber

## **Team Roles:**
[Define roles for each team member, such as developer, designer, project manager, QA tester, etc.]
- Brendon: Developer, QA Tester
- Michael: Developer, Project Manager
- Gavin: Developer

## **Team Norms:**
[Establish how the team will communicate, how often meetings will happen, and any other ground rules for collaboration.]
- We will communicate over Discord and in-person during class
- Meeting times will not be rigid, can schedule whenever works best for all members
    - Will try to meet at least once a week


## **Application Stack:**
[List all the technologies being used in the project, including programming languages, frameworks, and tools.]
- Python for model development
- Undecided for application interface

### **Libraries/Frameworks:**
[List any specific libraries or frameworks your application will use, such as React, Flask, Django, etc.]
- PyTorch