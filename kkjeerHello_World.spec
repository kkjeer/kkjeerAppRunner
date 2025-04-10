/*
A KBase module: kkjeerHello_World
*/

module kkjeerHello_World {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_kkjeerHello_World(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
