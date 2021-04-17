function Cp = pathGen(x0,xf,obst)

CONST.n = 8;
n = CONST.n;

loadVars;

xInit = init(CONST,x0,xf);

x = fmincon(@(x)costFun(CONST,x), xInit, [],[],[],[],[],[], @(x)nonlcon(CONST,x,x0,xf,obst));

x1 = [x0(1), x(1:n-1), xf(1)];
x2 = [x0(2), x(n:2*n-2), xf(2)];
x3 = [x0(3), x(2*n-1:3*n-3), xf(3)];
T = x(end);

Cp = [x1; x2; x3];

plot3(x1,x2,x3);