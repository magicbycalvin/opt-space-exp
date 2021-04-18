loadVars
Ts = CONST.Ts;

%rate = rosrate(CONST.Ts);

while(1)
    %% turtlebot routine
    %t = %current time
    turtlebot = 1;
    t_x0 = [0 0]';% initial position of turtlebot from ros
    t_xf = [10 10]';% next goal position
    obst = [5 5];% Generate obstacles array in form [o1x o1y; o2x o2y; ...]
    
    
    [t_Cp, t_T] = pathGen(CONST,t_x0,t_xf,obst,turtlebot);
    t_timeInfo = [t_t0, t_Tf, Ts];
    
    %% parrot routine
    %t = %current time
    turtlebot = 0;
    p_x0 = [0 10]';% initial position of turtlebot from ros
    p_xf = [10 0]';% next goal position
    obst = [];
    
    [p_Cp, p_T] = pathGen(CONST,p_x0,p_xf,obst,turtlebot);
    p_timeInfo = [p_t0, p_Tf, Ts];

end