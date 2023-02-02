/**
 Copyright [1999-2015] Wellcome Trust Sanger Institute and the EMBL-European Bioinformatics Institute
 Copyright [2016-2023] EMBL-European Bioinformatics Institute

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 **/


// Injects the GDPR notice onto sites
// For guidance on using: wwwdev.ebi.ac.uk/style-lab/websites/patterns/URL TO COME
function createDataProtectionBanner() {
    var banner = document.createElement('div');
    var wrapper = document.createElement('div');
    var inner = document.createElement('div');

    // don't accidently create two banners
    if (document.getElementById("data-protection-banner") != null) {
        document.getElementById("data-protection-banner").remove();
    }
    // status readout
    if (document.getElementById("data-protection-status") != null) {
        document.getElementById("data-protection-status").innerText += '\ncreating banner...';
    }

    banner.id = "data-protection-banner";
    banner.className = "cookie-banner";
    wrapper.className = "row";
    wrapper.innerHTML = "" +
        "<div class='swagger-ui-wrap' style='padding-left:20px;padding-right:20px;'>" +
        dataProtectionSettings.message +
        " <a target='_blank' href='" + dataProtectionSettings.link + "' class='white-color'>Privacy Notice</a>&nbsp;and&nbsp;<a target='_blank' href='" + dataProtectionSettings.termsofuse_link + "' class='white-color'>Terms of Use</a>&nbsp;&nbsp;" +
        "<a id='data-protection-agree' class='btn agree-button'>OK</a></div>" +
        "";

    document.body.appendChild(banner);
    banner.appendChild(wrapper);

    openDataProtectionBanner();
}

function openDataProtectionBanner() {
    var height = document.getElementById('data-protection-banner').offsetHeight || 0;
    document.getElementById('data-protection-banner').style.display = 'block';
    document.body.style.paddingBottom = height + 'px';

    document.getElementById('data-protection-agree').onclick = function () {
        closeDataProtectionBanner();
        return false;
    };
}

function closeDataProtectionBanner() {
    if (document.getElementById("data-protection-status") != null) {
        document.getElementById("data-protection-status").innerText += '\nclosing banner...';
    }

    var height = document.getElementById('data-protection-banner').offsetHeight;
    document.getElementById('data-protection-banner').style.display = 'none';
    document.body.style.paddingBottom = '0';
    setCookie(dataProtectionSettings.cookieName, 'true', 90);
}

function setCookie(c_name, value, exdays) {
    if (document.getElementById("data-protection-status") != null) {
        document.getElementById("data-protection-status").innerText += '\nsetting cookie for ' + dataProtectionSettings.cookieName + ' ...';
    }

    var exdate = new Date();
    var c_value;
    exdate.setDate(exdate.getDate() + exdays);
    // c_value = escape(value) + ((exdays===null) ? "" : ";expires=" + exdate.toUTCString()) + ";domain=.ebi.ac.uk;path=/";
    // document.cookie = c_name + "=" + c_value;
    c_value = escape(value) + ((exdays === null) ? "" : ";expires=" + exdate.toUTCString()) + ";domain=" + document.domain + ";path=/";
    document.cookie = c_name + "=" + c_value;
}

function getCookie(c_name) {
    var i, x, y, ARRcookies = document.cookie.split(";");
    for (i = 0; i < ARRcookies.length; i++) {
        x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
        y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x === c_name) {
            return unescape(y);
        }
    }
}

var dataProtectionSettings = new Object();

function runDataProtectionBanner() {
    dataProtectionSettings.message = 'This website requires cookies, and the limited processing of your personal data in order to function. By using the site you are agreeing to this as outlined in our ';
    dataProtectionSettings.link = 'https://www.ebi.ac.uk/data-protection/privacy-notice/transcript-archive-tark-';
    dataProtectionSettings.termsofuse_link = 'https://www.ebi.ac.uk/about/terms-of-use';
    //dataProtectionSettings.serviceId = 'ensembl-metadata';
    //dataProtectionSettings.dataProtectionVersion = '1.0';

    // If there's a div#data-protection-message-configuration, override defaults
    var divDataProtectionBanner = document.getElementById('data-protection-message-configuration');
    if (divDataProtectionBanner !== null) {
        if (typeof divDataProtectionBanner.dataset.message !== "undefined") {
            dataProtectionSettings.message = divDataProtectionBanner.dataset.message;
        }
        if (typeof divDataProtectionBanner.dataset.link !== "undefined") {
            dataProtectionSettings.link = divDataProtectionBanner.dataset.link;
        }
        if (typeof divDataProtectionBanner.dataset.serviceId !== "undefined") {
            dataProtectionSettings.serviceId = divDataProtectionBanner.dataset.serviceId;
        }
        if (typeof divDataProtectionBanner.dataset.dataProtectionVersion !== "undefined") {
            dataProtectionSettings.dataProtectionVersion = divDataProtectionBanner.dataset.dataProtectionVersion;
        }
    }

    //dataProtectionSettings.cookieName = dataProtectionSettings.serviceId + "-v" + dataProtectionSettings.dataProtectionVersion + "-data-protection-accepted";
    dataProtectionSettings.cookieName = "transcript-archive-tark-browsing"

    // If this version of banner not accpeted, show it:
    if (getCookie(dataProtectionSettings.cookieName) != "true") {
        createDataProtectionBanner();
    } else {
        if (document.getElementById("data-protection-status") != null) {
            document.getElementById("data-protection-status").innerText += '\nbanner for ' + dataProtectionSettings.cookieName + ' previously accepted, I won\'t show it...';
        }
    }

}

function resetDataProtectionBanner() {
    if (document.getElementById("data-protection-status") != null) {
        document.getElementById("data-protection-status").innerText += '\nreseting...';
    }

    document.cookie = dataProtectionSettings.cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT;domain=" + document.domain + ";path=/";

    runDataProtectionBanner();
}

if (document.getElementById("data-protection-status") != null) {
    document.getElementById("data-protection-status").innerText = '\nbootstraping...';
}

// execute
//runDataProtectionBanner();

