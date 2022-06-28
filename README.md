# Worktime Logger
Console based worktime logger to log the worked time for different projects

## Real Life Example:

### Start working on one or multiple projects

You start working on _Project_1_ (`s 0` or just `s`). Since this is programming work which you want to have logged all together, also start to log _Programming_ (`s 7`).
Because you're great in multitasking and work alone is boring, you start watching _Netflix_ in parallel (`s 10`).

### Have an overview of the current day's work

You see the running projects marked in the _Projects Overview_, as well in the _Current Progress Monitor_ with the progress bar filled:

Projects Overview    |  Current Progress Overview
:-------------------------:|:-------------------------:
![overview](https://user-images.githubusercontent.com/45213106/176210587-a126e9b9-b8cd-476e-8c5b-9400f419ba4c.PNG)  |  ![progress](https://user-images.githubusercontent.com/45213106/176210590-5f1b384a-aab4-432b-9bae-a9eacc4ccdc5.PNG)

If you want to see the inactive projects with a filled progress bar as well, type the command `fill`:

![progress_fill](https://user-images.githubusercontent.com/45213106/176211609-2b2c54ca-eb8e-4074-b7f7-c472f6332780.PNG)

### Be honest to yourself

You realise you're not so great as thought in multitasking and you can't work properly on _Project_1_ because Netflix is constantly asking if you're still watching. As a logical consequence, stop working on _Project_1_ and _Programming_ with `p` and `p 7`. Now you are able to enjoy Netflix without being interrupted by work:

![netflix](https://user-images.githubusercontent.com/45213106/176222312-03e4e695-6bd2-49c1-8ec6-cea1ae99922d.PNG)

After 2 hours, you will run out of Netflix time. To prevent yourself from watching Netflix for too long, use the command `c 10 6` to change the current _goal_ for Netflix to 6 hours and you're fine. For the next 4 hours.

![changed_goal](https://user-images.githubusercontent.com/45213106/176221816-83bb0118-eb44-4311-92e0-e3d3deb69dc8.PNG)

### Plot all your time worked on a project
Use the command `plot #` to generate and open a plot for the project number #:

![plot](https://user-images.githubusercontent.com/45213106/176224600-a055d69a-57fe-43a0-b3fa-d579a3ce77fe.png)

### Help

Use the command `help` to get an overview of all the commands available:

![help](https://user-images.githubusercontent.com/45213106/176223482-ce7a9eb1-8c1c-4595-b381-ef2e784178a5.PNG)

### Quit

Quit the _Worktime Logger_ with the command `q`. It will stop all running projects and print the today's log:

![quit](https://user-images.githubusercontent.com/45213106/176222958-89b641d3-4a66-4b9e-be7e-42ce738e3bed.PNG)

## Error handling
Error    |  Error handling
:-------------------------:|:-------------------------:
'temp_date.csv' permission error (write to file) | ![error_temp](https://user-images.githubusercontent.com/45213106/176232425-6797ef6a-343a-45a0-8f1c-e727a0e37714.PNG)
'main_date.csv' permission error (write to file) | ![error_main](https://user-images.githubusercontent.com/45213106/176231363-97986439-a851-4dd5-8022-03fccbc4dbeb.PNG)
pausing a project which is not running | ![error_pause](https://user-images.githubusercontent.com/45213106/176231489-547f0791-3bc7-4613-8cb6-694862137a05.PNG)
starting a project which is already running | ![error_start](https://user-images.githubusercontent.com/45213106/176231690-6454da34-3be9-4bf3-acdf-ea045b87ef69.PNG)



