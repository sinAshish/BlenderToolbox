a=[
0.001179	0.009332	0.059218	0.6271
0.00053	    0.005435	0.040368	1.309
0.00036	    0.005154	0.03517	    1.9953
0.000167	0.004145	0.025702	0.0354
0.000167	0.004137	0.02715	    0.1309
0.000166	0.004102	0.026583	0.5093]


close
semilogy(a(1:3,4),a(1:3,1),'o:','LineWidth',2)
hold on
semilogy(a(1:3,4),a(1:3,2),'x:','LineWidth',2)
semilogy(a(1:3,4),a(1:3,3),'+:','LineWidth',2)

semilogy(a(4:6,4),a(4:6,1),'o:','LineWidth',2)
semilogy(a(4:6,4),a(4:6,2),'x:','LineWidth',2)
semilogy(a(4:6,4),a(4:6,3),'+:','LineWidth',2)
ylabel loss
xlabel MB
legend({'D Loss1','D Loss2','D Loss3','INR Loss1','INR Loss2','INR Loss3'})
grid on