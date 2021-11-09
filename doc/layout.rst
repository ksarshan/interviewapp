Interview App
===================

Scheduling interviews is a burden in most of the companies. When you want to schedule
multiple interviews in a single day, It depends on the availability of the interviewer and
candidate.


Problem
**************

It would be wonderful if there is an API with which an interviewer/candidate can register their
available time period.

Say for example a candidate/interviewer is available on 2nd May from 10AM to 2PM. He should
be able to register this time slot using the API.
An HR manager should be able to get possible interview time slots by inputting both Candidate
ID and Interviewer ID to another API.

So using Python and Django,
    1. Write an API for candidates/interviewers to register their available time slots
    2. Write another API which will return interview schedulable time slots as a list which will take candidate id and interviewer id as input.

For example:
    If an interviewer is available from 9am to 12 pm, and a candidate is available
    from 11am to 2pm. Then the possible time slots will be [(10, 11), (11, 12)]


Solution
********

1. register candidate / Interviewer
    Sign up in with email

2.  HR is considered a super user

3. Picking the time slots
    - fix the length of interview as 1 hr
    - Candidate and Interviewer should pick the available time slots
    - HR manager should be able to get possible interview time slots by inputting both Candidate ID and Interviewer ID to another API.


Improvements
**********

1.  Can you suggest a better solution to the above mentioned interview scheduling problem?

    - If the interviewer is  available at the time of candidate registration, we can automatically schedule the interview
    - Interview update and cancellation option
    - Update engaged timeslots of interviewer as unavailable time or busy time

2   If you had some more time how would you improve your solution?

    - Cancellation is possible
    -  The authorization tokens of the user should be place in Redis and validate the token using a custom
       middleware or a decorator (avoid the db hit)
    -  Implement celery for the background task (eg auto scheduling)






