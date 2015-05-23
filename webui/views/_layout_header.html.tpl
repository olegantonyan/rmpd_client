<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="RMPD client web interface slon-ds.ru">
    <title>RMPD Web UI {{ g['rmpd_login'] }}</title>

    <link rel="stylesheet" href="static/pure/pure-min.css">
    <!--[if lte IE 8]>
        <link rel="stylesheet" href="static/css/layouts/side-menu-old-ie.css">
    <![endif]-->
    <!--[if gt IE 8]><!-->
        <link rel="stylesheet" href="static/css/layouts/side-menu.css">
    <!--<![endif]-->
</head>
<body>

<div id="layout">
    <!-- Menu toggle -->
    <a href="#menu" id="menuLink" class="menu-link">
        <!-- Hamburger icon -->
        <span></span>
    </a>

    <div id="menu">
        <div class="pure-menu pure-menu-open">
            <a class="pure-menu-heading" href="https://server.slon-ds.ru">slon-ds</a>
            <ul>
                % page_home_class = ''
                % page_status_class = ''
                % page_settings_class = ''
                % if get('page_home', False):
                %   page_home_class += 'pure-menu-selected'
                % end
                % if get('page_status', False):
                %   page_status_class += 'pure-menu-selected'
                % end
                % if get('page_settings', False):
                %   page_settings_class += 'pure-menu-selected'
                % end
                <li class="{{page_home_class}}"><a href="/">Home</a></li>
                <li class="{{page_status_class}}"><a href="/status">Status</a></li>
                <li class="{{page_settings_class}}"><a href="/settings">Settings</a></li>
            </ul>
        </div>
    </div>
    
    <div id="main">
    <div class="header">
        <h1>Media Player "{{ g['rmpd_login'] }}"</h1>
        <h2>slon-ds.ru media player web ui</h2>
    </div>
    
    <div class="content">