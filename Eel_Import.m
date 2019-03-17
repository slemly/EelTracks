clear
dist_threshold = 9/200;
dims = 4; %must be 4, or code to determine direction must be changed
Fname = 'D:\\Documents\\MATLAB\\Eel_Project\\output'; 
FtoImport = dir(fullfile(Fname));
FtoImport = FtoImport (3:end,:);
Eel_movements = cell (size (FtoImport,1),2);
for i = 1:size (FtoImport,1)
    i %progress indicator
    Datafile = FtoImport(i).name;
    Runname = regexp(Datafile,'[^_]*','match');
    Runname = Runname {1};
    Eel_movements (i,1) = {Runname};
    ImpFname = strcat (Fname,"\\",FtoImport(i).name);
    Coords = eel_import_file (ImpFname);
    Coords = Coords (:,3:4);
    %Coords = [Coords zeros(size (Coords,1),2);]; %#ok<AGROW>
    %3rd column distance, 4th column path
    %in degrees from previous
    mov_vect = zeros(1,size(Coords,1),'uint8');
    mov_vect_ind = 1;
    dist = 0;
    residual_dist = 0;
    %residual distance beyond the threshold, to add to the next series; 
    C1 = Coords (1,1:2);
    for i2 = 1:size (Coords,1) - 1
        C2 = Coords (i2+1,1:2);
        dist = pdist ([C1;C2]);
        dist = dist + residual_dist; 
        residual_dist = 0;
        if dist > dist_threshold
            %Find direction between first and last point to record, 
            %if distance travelled is greater than the threshold
            residual_dist = dist - dist_threshold;
            if residual_dist > dist_threshold
                debug = 'resdist>dist_threshold' %#ok
            end
            dir = atan2 (C2(2)-C1(2),C2(1)-C1(1)) / pi;
            if abs (dir) > 0.75
                %this must be changed to appropriate thresholds if dims not
                %4
                movcoord = 4;
            elseif abs (dir) < 0.25
                movcoord = 2;
            else
                if dir > 1
                    movcoord = 1;
                else
                    movcoord = 3; 
                end
            end
            mov_vect (mov_vect_ind) = movcoord;
            mov_vect_ind = mov_vect_ind + 1;
            dist = dist - dist_threshold;
            C1 = C2;
        end    
    end
    mov_vect = mov_vect (1:mov_vect_ind-1);
    Eel_movements (i,2) = {mov_vect};
    %save to cell array with label
    
end
save ('Eel_movements2','Eel_movements');

