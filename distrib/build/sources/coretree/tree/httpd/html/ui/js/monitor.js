// This is a genericized asynch data fetcher. It is intended to facilitate
//   simple asynch command and data passing between the server and the
//   browser.

// This code is largely stolen from bandwidthbars.cgi and is licensed
//   and copyrighted under the same terms.


// function simpleMonitor() kicks off an asynch HTTP request to the server.
//   when it's done, it calls the callback function with the rec'd text.
function simpleMonitor(httpReqObject, url, callback)
{
        var xmlHttpReq = false;
        var self = this;


        if (window.XMLHttpRequest) {
                // Mozilla/Safari
                httpReqObject = new XMLHttpRequest();
        } else if (window.ActiveXObject) {
                // IE
                httpReqObject = new ActiveXObject("Microsoft.XMLHTTP");
        }

        httpReqObject.open('GET', url, true);
        httpReqObject.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

        httpReqObject.onreadystatechange = function() {
                if ( httpReqObject && httpReqObject.readyState == 4) {
                        callback(httpReqObject.responseText);
                }
        }

        //document.getElementById('status').style.display = "inline";

        httpReqObject.send( null );
}


// Function no_op(): a callback when we expect nothing from the server or we
//   don't care about the data.
function no_op() { }
