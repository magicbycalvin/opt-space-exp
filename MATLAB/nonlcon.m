function [c,ceq] = nonlcon(CONST,x,x0,xf,obst)

n = CONST.n;
vmax = CONST.vmax;
vmin = CONST.vmin;
amax = CONST.amax;
amin = CONST.amin;
dsafe = CONST.dsafe;


x1 = [x0(1), x(1:n-1), xf(1)];
x2 = [x0(2), x(n:2*n-2), xf(2)];
x3 = [x0(3), x(2*n-1:3*n-3), xf(3)];
T = x(end);

[~,~,Dm] = BeBOT(n,T);

[numObst, ~] = size(obst);
dsqr = zeros(numObst,2*n+1);

for i = 1:numObst
    dsqr(i,:) = BernsteinProduct(x1-obst(i,1),x1-obst(i,1))+...
        BernsteinProduct(x2-obst(i,2),x2-obst(i,2))+...
        BernsteinProduct(x3-obst(i,3),x3-obst(i,3));
end
[row, col] = size(dsqr);
dsqr_row = reshape(dsqr,1,row*col);

Cp = [x1; x2; x3];
Cpdot = Cp*Dm;
Cpddot = Cp*Dm;

dx1 = Cpdot(1,:);
dx2 = Cpdot(2,:);
dx3 = Cpdot(3,:);

ddx1 = Cpddot(1,:);
ddx2 = Cpddot(2,:);
ddx3 = Cpddot(3,:);

vsqr = BernsteinProduct(dx1,dx1)+BernsteinProduct(dx2,dx2)+...
    BernsteinProduct(dx3,dx3);

asqr = BernsteinProduct(ddx1,ddx1)+BernsteinProduct(ddx2,ddx2)+...
    BernsteinProduct(ddx3,ddx3);

c = [-vsqr+vmin^2, vsqr-vmax^2, -dsqr_row+dsafe^2];
ceq = 0;
