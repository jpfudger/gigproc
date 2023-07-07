// vi: foldmethod=indent

function next_link() {
    var href = window.location.href
    var old = href.match(/\w+\.html/)
    
    var source = this.document.body.innerHTML
    var match = RegExp(old[0]).exec(source);
    if ( match ) {
        var source = source.substring(match.index+old[0].length)
        var next = /\w+\.html/.exec(source)

        if ( next ) {
            var new_url = href.replace(old[0], next[0])
            open_url(new_url)
            };

        };
    };

function prev_link() {
    var href = window.location.href
    var old = href.match(/\w+\.html/)
    
    var source = this.document.body.innerHTML
    var match = RegExp(old[0]).exec(source);
    if ( match ) {
        var source = source.substring(0,match.index)
        var regex = /(\w+\.html)/g
        var tmp;
        var prev;
        do {
            prev = tmp;
            tmp = regex.exec(source);
        } while ( tmp );

        if ( prev ) {
            var new_url = href.replace(old[0], prev[0])
            open_url(new_url)
            };

        };
    };

function next_link_new() {
    var href = window.location.href
    var old = href.match(/\w+\.html/)
    var source = this.document.body.innerHTML
    var source = source.replace(/\r?\n|\r/g,"")
    var regex = old[0] + ".+?" + "(\\w+\\.html)"
    var next = RegExp(regex).exec(source)
    if ( next ) {
        var url = href.replace(old[0], next[1])
        open_url(url)
        }

    };

function text_in_page(pattern) {
    var splits = pattern.split("/")
    var fname = splits[splits.length - 1]
    var source = document.body.innerHTML
    return source.match(fname)
    };

function open_url(url, docheck) {
    var check = true;
    if ( typeof docheck === "undefined" ) {
        check = true;
        }
    else if ( !docheck ) {
        check = false;
        }
    if ( !check || text_in_page(url) ) {
        this.document.location.href = url
        }
    };

function next_gig_url() {
    var href = window.location.href 
    var old_fname = href.match(/(\d\d)(\d\d)(\.html)/)
    var new_fname = old_fname[1] + String(Number(old_fname[2])+1).padStart(2,"0") + old_fname[3]
    var new_url = href.replace(old_fname[0], new_fname)
    return new_url
    };

function prev_gig_url() {
    var href = window.location.href 
    var old_fname = href.match(/(\d\d)(\d\d)(\.html)/)
    var new_fname = old_fname[1] + String(Number(old_fname[2])-1).padStart(2,"0") + old_fname[3]
    var new_url = href.replace(old_fname[0], new_fname)
    return new_url
    };

function next_year_url() {
    var href = window.location.href 
    var old_fname = href.match(/(\d\d)(\d\d)(\.html)/)
    var new_fname = String(Number(old_fname[1])+1) + "01" + old_fname[3]
    var new_url = href.replace(old_fname[0], new_fname)
    return new_url
    };

function prev_year_url() {
    var href = window.location.href 
    var old_fname = href.match(/(\d\d)(\d\d)(\.html)/)
    var new_fname = String(Number(old_fname[1])-1) + "01" + old_fname[3]
    var new_url = href.replace(old_fname[0], new_fname)
    return new_url
    };

function toggle_entry(id) {
    var uls = document.getElementsByTagName("ul");
    for ( var i=0; i<uls.length; i++ )
        {
        if ( uls[i].id == id )
            {
            if ( uls[i].style.display == "block" )
                {
                uls[i].style.display = "none";
                }
            else
                {
                uls[i].style.display = "block";
                }
            break;
            }
        }

    // don't do default event action, (i.e. reloading page)
    event.preventDefault();
    }

function toggle_image_visibility() {
    var image = document.getElementById("img");
    if ( image.style.display == "block" )
        { image.style.display = "none"; }
    else
        { image.style.display = "block"; }
    }

function toggle_image_cookie() {
    if ( get_image_cookie() )
        { del_image_cookie(); }
    else
        { set_image_cookie(); }

    }

shortcut.add("j",function() {
    next_link();
	// var url = next_gig_url();
    // open_url(url);
    });

shortcut.add("k",function() {
    prev_link();
	// var url = prev_gig_url();
    // open_url(url);
    });

shortcut.add("h",function() {
	var url = prev_year_url();
    open_url(url, false);
    });

shortcut.add("l",function() {
	var url = next_year_url();
    open_url(url, false);
    });

shortcut.add("a",function() {
    var href = window.location.href 
    var old_fname = href.match(/(\w+\.html)/)
    var url = href.replace(old_fname[0], "artists.html")
    open_url(url);
    });

shortcut.add("v",function() {
    var href = window.location.href 
    var old_fname = href.match(/(\w+\.html)/)
    var url = href.replace(old_fname[0], "venues.html")
    open_url(url);
    });

shortcut.add("g",function() {
    var href = window.location.href 
    var old_fname = href.match(/(\w+\.html)/)
    var url = href.replace(old_fname[0], "graphs.html")
    open_url(url);
    });

shortcut.add("c",function() {
    var href = window.location.href 
    var old_fname = href.match(/(\w+\.html)/)
    var url = href.replace(old_fname[0], "calendar.html")
    open_url(url);
    });

shortcut.add("i",function() {
    toggle_image_visibility()
    });


function set_image_cookie() { document.cookie = "ShowImages=1"; }
function get_image_cookie() { return document.cookie.includes("ShowImages=1"); }
function del_image_cookie() { document.cookie = "ShowImages=0"; }
    
function expand_cover_artist() // using url anchor
    {
    var anchor = window.location.href.match(/covers\.html#[^#]+$/)

    if ( anchor )
        {
        var anchor = anchor[0].slice(12);

        var lines = document.body.innerHTML.split("\n");

        for (var i=0; i<lines.length; i++)
            {

            if ( lines[i].includes(anchor) )
                {
                var index = lines[i+1].match(/toggle_entry\((\d+)\)/)[1]
                toggle_entry(index);
                break;
                }

            }
        }
    }
function set_image_visibility() // using cookie or url
    {

    show_images = get_image_cookie();

    if ( !show_images )
        {
        var local = window.location.href.match(/file:\/\//);
        var iparm = window.location.href.match(/\?i=1/);
        show_images = local || iparm;
        }

    if ( show_images )
        {
        document.getElementById("img").style.display = "block";
        }
    }

function process_url() {
    expand_cover_artist();
    set_image_visibility();
    }

window.onload = process_url
