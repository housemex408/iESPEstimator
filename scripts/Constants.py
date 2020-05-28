# common
PROJECT = "Project"
VERSION = "Version"
DATE = "Date"
DATE_P = "Date_P"
T_MODULE = "T_Module"
T_LINE = "T_Line"
T_CC = "T_CC"
TASK = "Task"
TASK_LIST = ["BUG", "DOCS", "REFACTOR", "TESTING", "FEATURE", "UPGRADE", "RELEASE", "SUPPORT", "OTHER"]
PROJECT_LIST = [
  "angular/angular"
  ,"nodejs/node"
  ,"openstack/neutron"
  ,"vuejs/vue"
  ,"home-assistant/home-assistant"
  ,"tensorflow/tensorflow"
  ,"moby/moby"
  ,"gitlabhq/gitlabhq"
  ,"dotnet/orleans"
  ,"dotnet/roslyn"
  ,"ansible/ansible"
  ,"cloudfoundry/cli"
  ,"openstack/nova"
  ,"angular/angular.js"
  ,"auth0/lock"
  ,"kubernetes/kubernetes"
  ,"apache/mesos"
  ,"odin-lang/Odin"
  ,"NixOS/nixpkgs"
  ,"facebook/react"
  ,"Homebrew/brew"
  ,"openstack/cinder"
  ,"elastic/elasticsearch"
  ,"torvalds/linux"
  ,"cloudfoundry/cf-deployment"
  ,"OfficeDev/office-js"
]
OTHER_PROJECT_LIST = [
  "d3/d3"
    ,"socketio/socket.io"
    ,"webpack/webpack"
    ,"jekyll/jekyll"
    ,"kennethreitz/requests"
    ,"lodash/lodash"
    ,"typicode/json-server"
    ,"Unitech/pm2"
    ,"videojs/video.js"
    ,"plataformatec/devise"
    ,"facebook/jest"
    ,"webtorrent/webtorrent"
    ,"npm/npm"
    ,"Automattic/mongoose"
    ,"visionmedia/superagent"
    ,"keystonejs/keystone"
    ,"yabwe/medium-editor"
    ,"jgm/pandoc"
    ,"swagger-api/swagger-ui"
    , "SeleniumHQ/selenium"
    ,"BrowserSync/browser-sync"
    ,"jhipster/generator-jhipster"
    ,"karma-runner/karma"
    ,"jsdom/jsdom"
    ,"stylus/stylus"
    ,"NetEase/pomelo"
    ,"systemjs/systemjs"
    ,"jordansissel/fpm"
    ,"nightwatchjs/nightwatch"
    ,"danialfarid/ng-file-upload"
    ,"NaturalNode/natural"
    ,"datproject/dat"
    ,"middleman/middleman"
    ,"fluent/fluentd"
    ,"zloirock/core-js"
    ,"vega/vega"
    ,"josdejong/mathjs"
    ,"AutoMapper/AutoMapper"
]

ALL_PROJECTS = PROJECT_LIST + OTHER_PROJECT_LIST

T_RECORDS = "T_Records"
D_RECORDS = "D_Records"
P_NA = "P_NA"
NT = "NT"
NO = "NO"
LINE = "Line"
MODULE = "Module"
T_CONTRIBUTORS = "T_Contributors"

# core contributor
NT_CC = "NT_CC"
NO_CC = "NO_CC"
MODULE_CC = "Module_CC"
LINE_CC = "Line_CC"
T_CC = "T_CC"

# external contributor
NT_EC = "NT_EC"
NO_EC = "NO_EC"
MODULE_EC = "Module_EC"
LINE_EC = "Line_EC"
T_EC = "T_EC"

# unknown contributor
NT_UC = "NT_UC"
NO_UC = "NO_UC"
MODULE_UC = "Module_UC"
LINE_UC = "Line_UC"
T_UC = "T_UC"

# data analysis dynamic columns
OBSERVED = "Observed"
PREDICTED = "Predicted"
DIFFERENCE = "Difference"
PERCENT_ERROR = "Percent_Error"
PREDICTED_X = "Predicted_X"
DIFFERENCE_X = "Difference_X"
PERCENT_ERROR_X = "Percent_Error_X"

# results output columns
MODEL = "Model"
R_SQUARED = "R_Squared"
R_SQUARED_X = "R_Squared_X"
R_SQUARED_ADJ = "R_Squared_Adj"
MAE = "MAE"
MSE = "MSE"
RMSE = "RMSE"
PRED_25 = "PRED_25"
PRED_50 = "PRED_50"
PRED_25_X = "PRED_25_X"
PRED_50_X = "PRED_50_X"

# roi output columns
AMOUNT_INVESTED = "Amount_Invested"
AMOUNT_RETURNED = "Amount_Returned"
INVESTMENT_GAIN = "Investment_Gain"
ROI = "ROI"
ANNUALIZED_ROI = "Annualized_ROI"

# PR fields
CONTRIBUTIONS = "Contributions"
CONTRIBUTORS = "Contributors"
COMMENTS = "Comments"
COMMENTERS = "Commenters"
T_COMMITS = "T_Commits"

# Cost fields CC
AVG_MODULE_CONTRIBS_CC = "AVG_MODULE_CONTRIBS_CC"
HOURS_DIFF_CC = "HOURS_DIFF_CC"
CONTRIB_DIFF_CC = "CONTRIB_DIFF_CC"
BILLED_HOURS_CC = "BILLED_HOURS_CC"
COST_CC = "COST_CC"

# Cost fields EC
AVG_MODULE_CONTRIBS_EC = "AVG_MODULE_CONTRIBS_EC"
HOURS_DIFF_EC = "HOURS_DIFF_EC"
CONTRIB_DIFF_EC = "CONTRIB_DIFF_EC"
BILLED_HOURS_EC = "BILLED_HOURS_EC"
COST_EC = "COST_EC"
