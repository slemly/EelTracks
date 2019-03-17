clc; close all;

for eels=1:257
tracksDATA=dlmread(['E',num2str(eels),'_flocdata_reordered.txt'],'',0,2);

centX=tracksDATA(:,7); centY=tracksDATA(:,8); 
headX=tracksDATA(:,3); headY=tracksDATA(:,4);
tailX=tracksDATA(:,5); tailY=tracksDATA(:,6);

plot(centX,centY,'x'); axis equal; %hold on; plot(headX,headY,'rx'); plot(tailX,tailY,'gx')
hold all

end
