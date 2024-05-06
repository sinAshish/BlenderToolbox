close all
clear

SAMPLE = 1;
crp=0.2;

if SAMPLE == 1 % CW SLICE
    rng=0:8:56;
    A=imread('./cw_slice.jpg');
elseif SAMPLE==2  %WHOLE BODY MR
    rng=[0 2 8 20 40 200];
    A=imread("./whole_body_MR.jpeg")
end

A=mat2gray(mean(A,3));
sz=size(A);

if SAMPLE ==1
    A=A(round(crp*sz(1)):round((1-crp)*sz(1)) ,  round(crp*sz(2)):round((1-crp)*sz(2)));
elseif SAMPLE ==2
    A=A(round(crp*sz(1)):end , :);
end

subplot(1,length(rng),1);
imshow(A);
if SAMPLE ==1
    A=imlocalbrighten(A,1);
    A=imlocalbrighten(A,1);
else
    %A=imlocalbrighten(A,1);
end
n=2;
for k=rng
    if SAMPLE==2
        B=imread(['./WB_segs/smart_seg_overlay_',num2str(k),'.png']);
    else
        B=imread(['./CW_segs/smart_seg_overlay_',num2str(k),'.png']);
    end
    B=1-mat2gray(mean(B,3));
    B=B>0.2;
    B2=zeros([sz(1) sz(2) 3]);
    B2(:,:,1)=B;
    B2(:,:,2)=B;

    if SAMPLE == 1
        B2=B2(round(crp*sz(1)):round((1-crp)*sz(1)),round(crp*sz(2)):round((1-crp)*sz(2)),1:3);
    elseif SAMPLE ==2
        B2=B2(round(crp*sz(1)):end , :, 1:3);
    end

    C = imfuse(A,B2,'blend');
    subplot(1,length(rng)+1,n);
    n=n+1;
    imshow(C)
end
set(gcf, 'Units', 'normalized', 'Position', [0, 0, 1, 1]); % Maximize figur
