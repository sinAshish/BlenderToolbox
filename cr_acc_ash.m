a = [
0.0354	144640	0.0019	0.000167	0.004145	0.025702	27.68361582    
0.1309	124836	0.00143	0.000167	0.004137	0.02715	7.486631016
0.5093	115728	0.00119	0.000166	0.004102	0.026583	1.9242097
0.0457	1500	0.00183	0.015409	0.040096	0.267702	21.44420131
0.1621	5000	0.00168	0.004308	0.01916	0.123641	6.045650833
0.6674	20000	0.00175	0.001106	0.009073	0.056477	1.468384777
]
close
semilogy(a(1:3,1),a(1:3,3),'o:','LineWidth',2)
hold on
semilogy(a(1:3,1),a(1:3,4),'x:','LineWidth',2)
semilogy(a(1:3,1),a(1:3,5),'+:','LineWidth',2)
semilogy(a(1:3,1),a(1:3,7),'x:','LineWidth',2)

semilogy(a(4:6,1),a(4:6,3),'o:','LineWidth',2)
semilogy(a(4:6,1),a(4:6,4),'x:','LineWidth',2)
semilogy(a(4:6,1),a(4:6,5),'+:','LineWidth',2)
semilogy(a(4:6,1),a(4:6,7),'x:','Linewidth',2)
ylabel Loss
xlabel Size(MB)

legend({'INR CD',' INR Edge','INR Laplacian','INR Compression','Mesh CD','Mesh Edge', 'Mesh Laplacian', 'Mesh Compression'})
grid on