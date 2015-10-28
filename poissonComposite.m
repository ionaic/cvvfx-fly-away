function [S, T, C] = poissonComposite(src, target, smask, tmask)
% A poisson image editing implementation.  This takes the names of the
% source, target, and mask images to be loaded and used

    % read in the source, target, and mask
    S = imread(src);
    T = imread(target);
    M = imread(smask);
    TM = imread(tmask);
    
    %omega is the region of interest, d-omega is the border just
    %outside the region of interest
    
    %we are trying to find a modification amount to make the entirety of
    %the omega region similar to the target by making d-omega the same as
    %the target
    
    %this is done by minimizing the difference in gradient, which equates
    %to finding when the difference in the derivatives (actually the 
    %gradients) of the gradients (the laplacian) is 0
    
    %to solve this system, find the E values, need to solve the system Ax =
    %b where A is the laplacian returned conveniently by delsq and x is the
    %column vector of pixels in omega
    
    [bound_x, bound_y] = find(M(:,:,1));
    bbox = [min(bound_y), min(bound_x), max(bound_y)-min(bound_y), max(bound_x)-min(bound_x)];
    nhood = [0, 1, 0; 1, 1, 1; 0, 1, 0];    
    
    %M2 = imerode(M, nhood);
    %dW = M2 - M; % d omega, the boundary
    %W = M2; % omega, the region
    
    % crop to the desired region
    M_crop = imcrop(M, bbox);
    S_crop = imcrop(S, bbox);
    T_crop = imcrop(T, bbox);
    
    % make the cropped mask logical and black and white
    M_crop = logical(im2bw(M_crop(:,:,1)));
    loc = find(M_crop);
    M_crop = double(M_crop);
    M_crop(loc) = 1:size(loc);
    %M_crop = double(logical(M_crop));
    %loc = find(M_crop);
    %size(loc)
    %M_crop(loc) = 1:size(loc);
    imshow(M_crop)
    size(M_crop)
    lapl = delsq(M_crop);

    E = T_crop - S_crop;
    size(E)
    %delE = E;
    delE = zeros(size(E));
    %tmp = double(lapl) * double(E(loc));
    %size_eig = size(eig(tmp))
    delE(loc) = double(lapl) * double(E(loc));
    C = T;
    I = S_crop + uint8(delE);
    imshow(I)
    %imshow(TM)
    %size_cbbox = size(C(min(cby):max(cby), min(cbx):max(cbx), :))
    %C(min(cby):max(cby), min(cbx):max(cbx), :) = I;
    %Cbbox = C(min(bound_y):max(bound_y), min(bound_x):max(bound_x),:);
    %C(min(bound_x):max(bound_x), min(bound_y):max(bound_y),:) = I;
    size(find(logical(im2bw(TM))))
    size(find(M_crop))
    C(find(logical(im2bw(TM)))) = I(find(M_crop));
    S = S_crop;
    T = T_crop;
end