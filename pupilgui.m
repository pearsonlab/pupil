function varargout = pupilgui(varargin)
% PUPILGUI MATLAB code for pupilgui.fig
%      PUPILGUI, by itself, creates a new PUPILGUI or raises the existing
%      singleton*.
%
%      H = PUPILGUI returns the handle to a new PUPILGUI or the handle to
%      the existing singleton*.
%
%      PUPILGUI('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in PUPILGUI.M with the given input arguments.
%
%      PUPILGUI('Property','Value',...) creates a new PUPILGUI or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before pupilgui_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to pupilgui_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help pupilgui

% Last Modified by GUIDE v2.5 04-Apr-2014 16:08:36

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @pupilgui_OpeningFcn, ...
                   'gui_OutputFcn',  @pupilgui_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before pupilgui is made visible.
function pupilgui_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to pupilgui (see VARARGIN)

% Choose default command line output for pupilgui
handles.output = hObject;

% setup paths
addpath('~/code/pupil/analysis')
addpath('~/code/pupil/analysis/utils')
addpath('~/code/electrophysiology')
handles.ddir = '~/data/pupil/';

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes pupilgui wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = pupilgui_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
if isfield(handles, 'curr_data_dir')
    [dfile, curr_data_dir, was_success] = ...
        uigetfile([handles.curr_data_dir '*.mat']);
else
    [dfile, curr_data_dir, was_success] = uigetfile([handles.ddir '*.mat']);
end

handles.dfile = dfile;
handles.curr_data_dir = curr_data_dir;

guidata(hObject, handles);

do_analysis(hObject, eventdata, handles)

function do_analysis(hObject, eventdata, handles)
dfile = handles.dfile;
newdir = handles.curr_data_dir;

prepdata

% set options
normtype = 0;  % 0 for subtractive, 1 for divisive
overplot = 0;  % 0 produces a new plot, 1 plots into existing axes
plottype = 1;  % 0 for no sem, 1 for error shading, 2 for dotted lines
include_tonic = 1;

% run task-specific analysis
if ~overplot
    fig_handle = figure;
    if include_tonic
        pos = get(fig_handle, 'position');
        pos(4) = 2 * pos(4);
        set(fig_handle, 'position', pos);
        
        subplot(2, 1, 2);
        plot(taxis, pupil, 'color', 'k', 'linewidth', 2)
        xlabel('Time (seconds)', 'fontsize', 16, 'fontweight', 'bold')
        ylabel('Raw pupil size (arb units)', 'fontsize', 16, 'fontweight', 'bold')

        subplot(2, 1, 1);
    end
end

switch task
    case 'darktest'
        analyze_darktest
    case 'lighttest'
        analyze_lighttest
    case 'revlearn'
        analyze_revlearn
    case 'oddball'
        analyze_oddball
    case 'pst'
        analyze_pst
end
