
function neuron = df(filename)
    % Open the SWC file
    fid = fopen(filename, 'r');
    if fid == -1
        error('Unable to open file: %s', filename);
    end
    
    % Read the SWC file line by line
    lines = {};
    while ~feof(fid)
        line = fgetl(fid);
        if ~isempty(line)
            lines{end+1} = line;
        end
    end
    fclose(fid);
    
    % Initialize matrix to store neuron data
    num_segments = numel(lines);
    neuron = zeros(num_segments, 7);
    
    % Parse each line and fill the matrix
    for i = 1:num_segments
        line = strsplit(lines{i});
        neuron(i, 1) = str2double(line{2});  % ID
        neuron(i, 2) = str2double(line{3});  % Type
        neuron(i, 3) = str2double(line{4});  % X
        neuron(i, 4) = str2double(line{5});  % Y
        neuron(i, 5) = str2double(line{6});  % Z
        neuron(i, 6) = str2double(line{7});  % Radius
        neuron(i, 7) = str2double(line{8});  % Parent ID
    end
    
    % Draw the neuron
    grid on % Turns grid on.
    hold on
    view([-45 30])

    for Pnt=2:size(neuron,1); % For all line segments in vessel tree.
        PntX=neuron(Pnt,3); PntY=neuron(Pnt,4); PntZ=neuron(Pnt,5);
        % Establish current point locations.

        PntConn=neuron(Pnt,7);
        PntConnX=neuron(PntConn,3); PntConnY=neuron(PntConn,4); PntConnZ=neuron(PntConn,5);
        % Establish connecting point locations.

        if (neuron(Pnt,2)==0), ColourString='r'; else ColourString='k'; end;
        % This colours the vessels according to vessel classification. This
        % defaults to black for vessels from the orginal vessel tree and red
        % for vessels generated or split from vessel generation.

        plot3([PntConnY PntY],[PntConnX PntX],[PntConnZ PntZ],ColourString);
        % Plot vessel lines.

        drawnow limitrate % Updates figure as it loops.
    end
    drawnow % Finalises figure.

    

end

