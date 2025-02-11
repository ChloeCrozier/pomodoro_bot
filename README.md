# Pomodoro Bot
A bot that allows for collaborative study sessions within Discord servers. The planned functionality is that one user can start a timer by calling !start. Users who want to join that session can react to the original user's message with a like. All users in the session will have permissions to pause and change the duration mode.

Timer Modes:
- Work: The session starts with a 25-minute work timer. After each work period, a break will follow, and then another work period begins.
- Short Break: After the first three work periods, a 5-minute short break will occur.
- Long Break: A 15-minute long break is triggered after every four work periods.
- 
Commands:
- !start-session: Starts a new study session.
- !end-session: Ends the timer, resets the counters, and summarizes your session’s study metrics.
- !pause: Pauses the timer for all users within the session.
- !unpause: Resumes the timer for all users within the session.
- !set-time: Allows you to set the work, long break, and short break durations.
- !next: Increments the study counter (for completed sessions) and progresses to the next timer mode.
- !reset: Restarts the current mode duration to the starting time.
