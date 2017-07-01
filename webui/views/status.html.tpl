% include('_layout_header.html.tpl', page_status=True)

<h2 class="content-subhead">Status</h2>
<table class="pure-table pure-table-horizontal">
    <tbody>
        <tr>
            <td>Device login</td>
            <td>{{g['rmpd_login']}}</td>
        </tr>
        <tr>
            <td>Now playing</td>
            <td>{{now_playing}}</td>
        </tr>
        <tr>
            <td>Online?</td>
            <td>{{ "yes" if online else "no" }}</td>
        </tr>
        <tr>
            <td>Static IP</td>
            <td>{{static_ip}}</td>
        </tr>
        <tr>
            <td>Ethernet IP</td>
            <td>{{ethernet_ip}}</td>
        </tr>
        <tr>
            <td>WiFi IP</td>
            <td>{{wifi_ip}}</td>
        </tr>
    </tbody>
</table>

% include('_layout_footer.html.tpl')