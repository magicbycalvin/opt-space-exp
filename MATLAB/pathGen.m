function [Cp, T] = pathGen(CONST,x0,xf,obst,turtlebot)
n = CONST.n;

xInit = init(CONST,x0,xf);

x = fmincon(@(x)costFun(CONST,x), xInit, [],[],[],[],[],[], @(x)nonlcon(CONST,x,x0,xf,obst,turtlebot));

x1 = [x0(1), x(1:n-1), xf(1)];
x2 = [x0(2), x(n:2*n-2), xf(2)];
%x3 = [x0(3), x(2*n-1:3*n-3), xf(3)];
T = x(end);

%Cp = [x1; x2; x3];
Cp = [x1; x2];

% %plot3(x1,x2,x3);
% plot(x1,x2); hold on
% %plot(obst(:,1),obst(:,2), 'ko');