# CS445: Software Engineering Guidelines

*A portion of your team's final project will be graded against these guidelines and specifications*
  
1. Software breaks at the interfaces
    * If you don't do a system architectural design with well-defined interfaces, integration will be a big mess.You must have some external system architecural design that is kept up to date with your current architecture.

2. Good software is in your head, not the computer
      * Design, Design, Design, then design some more. You should spend at least as much time designing your code, before you write a single line, as you will spend coding.

3. Try to make your development environment as close to your production environment as possible (without giving away secrets) 
     * Designing the running environment is as important as  designing project itself. Many projects require as much time setting up the running environment as they do for development.

4. "What takes 1 Dev one month to complete, will will take 2 devs two months, but will be better"
     * The more people on a project the longer it takes. Adding team members that are new to a project are less productive (1/3 to 2/3 less), so new devs add at minimum 1/3 more time to the timeline.

5. Productivity varies greatly depending knowledge of the tools, methods, and notations used
      * Invest time in Documentation. Don't write from scratch something that can be easily accomplished with a call to a library. 

6. Fluctuating and conflicting requirements reduces software productivity and quality  
      * Each time a component or requirements changes, the amount of work to integrate the change is proportional to how much of the project has already been completed.

7. The earlier problems are discovered, the less the overall cost will be.
      * The client meeting to determine how the software will be used is the most imporant meeting in the software development process. No matter how good your software is, if it doesn't meet the client's needs, it is an unsuccessful software product. 

8. Once a requirement is met, it should be considered frozen until project completion.
      * If requirements are not locked on completion, the project risks feature creep. **Feature Creep** entails constantly adding new capabilities to existing features, rather than tackling incomplete requirements.

9. Separate the things that change from the things that stay the same
      * This applys when talking about single functions or entire applications. Always ask, what may change here and how do I minize that changes impact. 
