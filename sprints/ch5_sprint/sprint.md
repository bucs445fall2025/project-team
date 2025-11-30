# Sprint Meeting Notes

*note: replace anything surrounded by << >> and **remove** the << >>*

**Attended**: Brendon, Michael, Gavin

**DATE**: 10/13/25

***

## Sprint 2 Review

### SRS Sections Updated

- Requirements

### User Story

- stock_prediction_story.md

### Sprint Requirements Attempted

- Cost requirement (API caching/database)

### Completed Requirements

- Storage
    - Database setup
    - R/W operations
    - Caching for API endpoints

### Incomplete Requirements

- N/A

### The summary of the entire project

- Stock tracker / future price prediction

***

## Sprint 3 Planning

## Requirements Flex

5/5 requirement flexes remaining

## Technical Debt

- None

### Requirement Target

- Data analysis

### User Stories

- stock_prediction_story.md

### Planning

- Train a linear regression model on daily stock data. This model will use daily post-Covid data to predict the next day's stock value. This will be our most basic model, so it is expected to be completed during this week's sprint alone.

### Action Items

- Implement a simple linear regression model for stock prediction

### Issues and Risks

- Compute time could be an issue. Our GPUs only include a 3070-Laptop and a 3060-Desktop.

### Team Work Assignments

- Linear regression model: Brendon
- Work on getting homepage done for website: Michael
- Work with brendon on figuring out how to store the results of the linear regression model: Gavin
- Setting up api calls to new database: Gavin
- Organize python classes: Brendon, Gavin, Michael
