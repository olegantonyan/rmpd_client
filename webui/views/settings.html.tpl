% include('_layout_header.html.tpl', page_settings=True)

<h2 class="content-subhead">Settings</h2>
                        
<form class="pure-form pure-form-aligned" action="/settings/change_ethernet_address" method="post">
    <fieldset>
        <legend>Ethernet network</legend>
        <div class="pure-controls">
            <label for="ethernet_use_dhcp" class="pure-checkbox">
                % ethernet_dhcp_state_checkbox = 'checked' 
                % ethernet_static_ip_control_mode = 'none'
                % if ethernet_addr_form_values['dhcp'] != True:
                %   ethernet_dhcp_state_checkbox = ''
                %   ethernet_static_ip_control_mode = 'block'
                %end
                <input id="ethernet_use_dhcp" name="use_dhcp" type="checkbox" {{ethernet_dhcp_state_checkbox}} onclick="toggle_div('ethernet_static_ip_controls', !this.checked);"> DHCP
                <script> function toggle_div(id, show) { document.getElementById(id).style.display = show ? 'block' : 'none'; } </script>
            </label>
        </div>
        <div id="ethernet_static_ip_controls" style="display:{{ethernet_static_ip_control_mode}};">
            <div class="pure-control-group">
                <label for="ethernet_addr">Address</label>
                <input id="ethernet_addr" name="addr" type="text" placeholder="Static IPv4 address (i.e. 192.168.1.25)" class="pure-input-2-3" value="{{ethernet_addr_form_values['addr']}}">
            </div>
        
            <div class="pure-control-group">
                <label for="ethernet_netmask">Netmask</label>
                <input id="ethernet_netmask" name="netmask" type="text" placeholder="Static IPv4 netmask (i.e. 255.255.255.0)" class="pure-input-2-3" value="{{ethernet_addr_form_values['netmask']}}">
            </div>
            
            <div class="pure-control-group">
                <label for="ethernet_gateway">Gateway</label>
                <input id="ethernet_gateway" name="gateway" type="text" placeholder="Static IPv4 gateway (i.e. 192.168.1.1)" class="pure-input-2-3" value="{{ethernet_addr_form_values['gateway']}}">
            </div>
            
            <div class="pure-control-group">
                <label for="ethernet_nameservers">Nameserver(s)</label>
                <input id="ethernet_nameservers" name="nameservers" type="text" placeholder="Static IPv4 DNS (i.e. 192.168.1.1, 8.8.8.8)" class="pure-input-2-3" value="{{ethernet_addr_form_values['nameservers']}}">
            </div>
        </div>
        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Submit</button>
        </div>
    </fieldset>
</form>

<form class="pure-form pure-form-aligned" action="/settings/change_wifi_address" method="post">
    <fieldset>
        <legend>WiFi network</legend>

        <div class="pure-control-group">
            <label for="wifi_ssid">SSID</label>
            <input id="wifi_ssid" name="ssid" type="text" placeholder="Network name" class="pure-input-2-3" value="{{wifi_addr_form_values['ssid']}}">
        </div>

         <div class="pure-control-group">
            <label for="wifi_psk">Password</label>
            <input id="wifi_psk" name="psk" type="text" placeholder="Network password" class="pure-input-2-3" value="{{wifi_addr_form_values['psk']}}">
        </div>

        <div class="pure-controls">
            <label for="wifi_use_dhcp" class="pure-checkbox">
                % wifi_dhcp_state_checkbox = 'checked' 
                % wifi_static_ip_control_mode = 'none'
                % if wifi_addr_form_values['dhcp'] != True:
                %   wifi_dhcp_state_checkbox = ''
                %   wifi_static_ip_control_mode = 'block'
                %end
                <input id="wifi_use_dhcp" name="use_dhcp" type="checkbox" {{wifi_dhcp_state_checkbox}} onclick="toggle_div('wifi_static_ip_controls', !this.checked);"> DHCP
                <script> function toggle_div(id, show) { document.getElementById(id).style.display = show ? 'block' : 'none'; } </script>
            </label>
        </div>

        <div id="wifi_static_ip_controls" style="display:{{wifi_static_ip_control_mode}};">
            <div class="pure-control-group">
                <label for="wifi_addr">Address</label>
                <input id="wifi_addr" name="addr" type="text" placeholder="Static IPv4 address (i.e. 192.168.1.25)" class="pure-input-2-3" value="{{wifi_addr_form_values['addr']}}">
            </div>
        
            <div class="pure-control-group">
                <label for="wifi_netmask">Netmask</label>
                <input id="wifi_netmask" name="netmask" type="text" placeholder="Static IPv4 netmask (i.e. 255.255.255.0)" class="pure-input-2-3" value="{{wifi_addr_form_values['netmask']}}">
            </div>
            
            <div class="pure-control-group">
                <label for="wifi_gateway">Gateway</label>
                <input id="wifi_gateway" name="gateway" type="text" placeholder="Static IPv4 gateway (i.e. 192.168.1.1)" class="pure-input-2-3" value="{{wifi_addr_form_values['gateway']}}">
            </div>
            
            <div class="pure-control-group">
                <label for="wifi_nameservers">Nameserver(s)</label>
                <input id="wifi_nameservers" name="nameservers" type="text" placeholder="Static IPv4 DNS (i.e. 192.168.1.1, 8.8.8.8)" class="pure-input-2-3" value="{{wifi_addr_form_values['nameservers']}}">
            </div>
        </div>
        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Submit</button>
        </div>
    </fieldset>
</form>

<form class="pure-form pure-form-aligned" action="/settings/change_password" method="post">
    <fieldset>
        <legend>Change admin password</legend>
        <div class="pure-control-group">
            <label for="current_password">Current password</label>
            <input id="current_password" type="password" placeholder="Current password" name="current_password" class="pure-input-2-3">
        </div>
        <div class="pure-control-group">
            <label for="new_password">New password</label>
            <input id="new_password" type="password" placeholder="New password" name="new_password" class="pure-input-2-3">
        </div>
        <div class="pure-controls">
            <button type="submit" class="pure-button pure-button-primary">Submit</button>
        </div>
    </fieldset>
</form>

% include('_layout_footer.html.tpl')