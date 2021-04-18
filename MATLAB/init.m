function xInit = init(CONST,x0,xf)

n = CONST.n;

x1Init = linspace(x0(1),xf(1),n-1);
x2Init = linspace(x0(2),xf(2),n-1);
%x3Init = linspace(x0(3),xf(3),n-1);
tInit = 10;

%xInit = [x1Init, x2Init, x3Init, tInit];
xInit = [x1Init, x2Init, tInit];