我現在想要改變menu跟app.vue裡面buttom bar的邏輯成下面這樣，整個安排應該會讓button bar變成
chat home nolification

## chat
- icon 
    + 正常
        <span class="material-icons-round">
            chat
        </span>
    + unread message
        <span class="material-icons-round">
            mark_unread_chat_alt
        </span>
- 選到之後要在icon上方出現 'Chat' 的小字
- 選擇之後跳轉到ChatList頁面

## Home
- 相較buttom bar的其他地方是平的，應該會相較是圓形
- icon
    <span class="material-icons-round">
        home
    </span>
- 選到後
    + 上方要出現 'Home的字樣'
    + 跟著上面的圓弧依序出現 'Profile' - 'Jobs' - 'Ｄashboard' - 'Community'
        - Profile
            + icon
                <span class="material-icons-round">
                    account_circle
                </span>
            + 選到的時候反白且浮'Profile'小字
            + 點按之後進到profile detail
        - Jobs
            + icon
                <span class="material-icons-round">
                    work
                </span>
            + 選到的時候反白且浮'Jobs'小字
            + 點按之後進到joblist
        - Dashboard
            + icon
                <span class="material-icons-round">
                    dashboard
                </span>
            + 選到的時候反白且浮'Dashboard'小字
            + 點按之後進到ApplicationList
        - Communitiy
            + icon
                <span class="material-icons-round">
                    groups
                </span>
            + 選到的時候反白且浮'Community'小字
            + 點按之後進到ProfileList
- 直接點選進homeview

## notification
- icon 
    + 正常
        <span class="material-icons-round">
            notifications
        </span>
    + unread message
        <span class="material-icons-round">
            notifications_active
        </span>
- 選到之後要在icon上方出現 'Notification' 的小字
- 選擇之後跳轉到notifiacation頁面