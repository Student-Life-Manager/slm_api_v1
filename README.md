### prathyushaa's todo list

- [x] approve outpasses on both levels - prathyushaa
- [ ] disable deleting guardians when an outpass is active
- [ ] lazy joining student and guardians to outpass details
- [ ] use student and warden decorator for guardian and outpass routes
- [ ] separate routes to view all outpasses for student and warden
- [ ] route to get outpasses by hostel name
- [ ] get all active outpasses for wardens or hostels
- [x] create outpasses using `seed_db.py` script - prathyushaa


### discussions 
- Do we need seperate checklist schemas for both student and warden? why?
- how to differentiate crud functions for different account types?
- want to setup sentry?
- do you want to setup testing? Maybe not because it will take a lot of time
- different encoding strategy for student and wardens? we can add user type in payload too
- different permissions for students and wardens if we do the above so its easier to block routes which are not meant for students


### deployment

- setup aws rds for postgres db (might need to setup ec2 not sure)
    - google cloud $300 credits for free

- ecs for deployment
    - 
