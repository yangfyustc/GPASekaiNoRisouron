################################################################################
## 初始化
################################################################################

init offset = -1


## 确认对话框是否显示
default persistent.confirmation_dialog = True
## 已读文本是否变色
default persistent.text_color_change = True
## 常规模式下文本显示速度
default persistent.text_displayspeed = 0
# ## 自动模式下文本显示速度
default persistent.text_autospeed = 50
## 文本框alpha
define persistent.textbox_alpha = 1.0
## 文本预览用
define speed_preview_repeat_time = 3.0
default countdown_time = 0.0
default text_read = True


#全设置恢复初始值
init python:
    def func_reset(value_reset):
        preferences.fullscreen = False
        preferences.transitions = 2
        persistent.confirmation_dialog = True
        preferences.mouse_move = False
        persistent.text_color_change = True
        preferences.wait_voice = True
        preferences.voice_sustain = True
        preferences.skip_unseen = True
        persistent.text_displayspeed = 0
        persistent.text_autospeed = 50
        persistent.textbox_alpha = 1.0
        preferences.text_cps = 40
        return



################################################################################
## 样式
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## 游戏内屏幕
################################################################################


## 对话屏幕 ########################################################################
##
## 对话屏幕用于向用户显示对话。它需要两个参数，who 和 what，分别是叙述角色的名字
## 和所叙述的文本。（如果没有名字，参数 who 可以是 None。）
##
## 此屏幕必须创建一个 id 为 what 的文本可视控件，因为 Ren'Py 使用它来管理文本显
## 示。它还可以创建 id 为 who 和 id 为 window 的可视控件来应用样式属性。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#say

screen say(who, what):

    #style_prefix "say"
    window:
        id "window"
        ## 文本框透明度
        background im.Alpha("gui/textbox.png", persistent.textbox_alpha)
        ## 文本显示速度
        $ preferences.text_cps = persistent.text_displayspeed

        if who is not None:
            window:
                id "namebox"
                ## 调节姓名框透明度 
                background im.Alpha("gui/namebox.png", persistent.textbox_alpha)
                style "namebox"
                text who id "who"

        ## 已读文本变色
        if persistent.text_color_change == True:

            ## 已被查看(不包括当前文本)
            if renpy.is_seen(ever = True):
                text what id "what" color  "#e29e3e" outlines [(2,"#00000088",0,0)]
            ## 未被查看
            else:
                text what id "what" outlines [(2,"#00000088",0,0)]

        ## 不允许已读文本变色
        else:
            text what id "what"
        # text what id "what"


    ## 如果有对话框头像，会将其显示在文本之上。请不要在手机界面下显示这个，因为
    ## 没有空间。
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

    key "mousedown_4" action ShowMenu('history') 
    #key "mouseup_3" action ShowMenu("save")


## 通过 Character 对象使名称框可用于样式化。
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    slow_abortable True  #点击鼠标后全部显现文本
    adjust_spacing False

## 输入屏幕 ########################################################################
##
## 此屏幕用于显示 renpy.input。prompt 参数用于传递文本提示。
##
## 此屏幕必须创建一个 id 为 input 的输入可视控件来接受各种输入参数。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## 选择屏幕 ########################################################################
##
## 此屏幕用于显示由 menu 语句生成的游戏内选项。参数 items 是一个对象列表，每个对
## 象都有字幕和动作字段。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 338
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## 快捷菜单屏幕 ######################################################################
##
## 快捷菜单显示于游戏内，以便于访问游戏外的菜单。

screen quick_menu():

    ## 确保该菜单出现在其他屏幕之上，
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.7
            yalign 1.0

            spacing 10

            imagebutton:
                idle "gui/button/game_on_auto.png"
                hover "gui/button/game_off_auto.png"
                selected_idle "gui/button/game_active_auto.png"
                selected_hover "gui/button/game_off_auto.png"
                action Preference("auto-forward", "toggle") 

            imagebutton:
                idle "gui/button/game_on_skip.png"
                hover "gui/button/game_off_skip.png"
                insensitive "gui/button/game_off_skip.png"
                selected_idle "gui/button/game_active_skip.png"
                selected_hover "gui/button/game_off_skip.png"
                action Skip() alternate Skip(fast=True, confirm=False)

            imagebutton:
                idle "gui/button/game_on_config.png"
                hover "gui/button/game_off_config.png"
                action ShowMenu('preferences')

            imagebutton:
                idle "gui/button/game_on_qsave.png"
                hover "gui/button/game_off_qsave.png"
                action QuickSave()

            imagebutton:
                idle "gui/button/game_on_qload.png"
                hover "gui/button/game_off_qload.png"
                action QuickLoad()

            imagebutton:
                idle "gui/button/game_on_save.png"
                hover "gui/button/game_off_save.png"
                action ShowMenu('save')
            
            imagebutton:
                idle "gui/button/game_on_load.png"
                hover "gui/button/game_off_load.png"
                action ShowMenu('load')

            imagebutton:
                idle "gui/button/game_on_log.png"
                hover "gui/button/game_off_log.png"
                action ShowMenu('history')

            imagebutton:
                idle "gui/button/game_on_close.png"
                hover "gui/button/game_off_close.png"
                action Call("_hide_windows")

            # textbutton _("回退") action Rollback()
            # textbutton _("历史") action ShowMenu('history')
            # textbutton _("快进") action Skip() alternate Skip(fast=True, confirm=persistent.confirmation_dialog)
            # textbutton _("自动") action Preference("auto-forward", "toggle")
            # textbutton _("保存") action ShowMenu('save')
            # textbutton _("快存") action QuickSave()
            # textbutton _("快读") action QuickLoad()
            # textbutton _("设置") action ShowMenu('preferences')


## 此代码确保只要用户没有主动隐藏界面，就会在游戏中显示 quick_menu 屏幕。
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## 标题和游戏菜单屏幕
################################################################################

## 导航屏幕 ########################################################################
##
## 该屏幕包含在标题菜单和游戏菜单中，并提供导航到其他菜单，以及启动游戏。

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("开始游戏") action Start()

        else:

            textbutton _("历史") action ShowMenu("history")

            textbutton _("保存") action ShowMenu("save")

        textbutton _("读取游戏") action ShowMenu("load")

        textbutton _("设置") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("结束回放") action EndReplay(confirm=persistent.confirmation_dialog)

        elif not main_menu:

            textbutton _("标题菜单") action MainMenu(confirm=True)

        if main_menu:

            textbutton _("关于") action ShowMenu("about")

        # if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## “帮助”对移动设备来说并非必需或相关。
            # textbutton _("帮助") action ShowMenu("help")

        if renpy.variant("pc"):

            ## 退出按钮在 iOS 上是被禁止使用的，在安卓和网页上也不是必要的。
            textbutton _("退出") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## 标题菜单屏幕 ######################################################################
##
## 用于在 Ren'Py 启动时显示标题菜单。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#main-menu

screen main_menu():

    ## 此语句可确保替换掉任何其他菜单屏幕。
    tag menu

    add gui.main_menu_background

    ## 此空框可使标题菜单变暗。
    frame:
        style "main_menu_frame"

    # ## use 语句将其他的屏幕包含进此屏幕。标题屏幕的实际内容在导航屏幕中。
    # use navigation

    vbox:
        xpos 30
        yalign 0.6

        spacing 10

        imagebutton:
            idle "gui/button/title_on_start.png"
            hover "gui/button/title_off_start.png"
            action Start()

        imagebutton:
            idle "gui/button/title_on_load.png"
            hover "gui/button/title_off_load.png"
            action ShowMenu("load")

        imagebutton:
            idle "gui/button/title_on_extra.png"
            hover "gui/button/title_off_extra.png"
            action [Stop('music'), ShowMenu("extra")]

        imagebutton:
            idle "gui/button/title_on_config.png"
            hover "gui/button/title_off_config.png"
            action ShowMenu("preferences")

        imagebutton:
            idle "gui/button/title_on_quit.png"
            hover "gui/button/title_off_quit.png"
            action Quit(confirm=True)

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

    key "game_menu" action NullAction()


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 350
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -25
    xmaximum 1000
    yalign 1.0
    yoffset -25

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## 游戏菜单屏幕 ######################################################################
##
## 此屏幕列出了游戏菜单的基本共同结构。可使用屏幕标题调用，并显示背景、标题和导
## 航菜单。
##
## scroll 参数可以是 None，也可以是 viewport 或 vpgrid。此屏幕旨在与一个或多个子
## 屏幕同时使用，这些子屏幕将被嵌入（放置）在其中。

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## 导航部分的预留空间。
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("返回"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 38
    top_padding 150

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 350
    yfill True

style game_menu_content_frame:
    left_margin 50
    right_margin 25
    top_margin 13

style game_menu_viewport:
    xsize 1150

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 13

style game_menu_label:
    xpos 63
    ysize 150

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -37


## 关于屏幕 ########################################################################
##
## 此屏幕提供有关游戏和 Ren'Py 的制作人员和版权信息。
##
## 此屏幕没有什么特别之处，因此它也可以作为一个例子来说明如何制作一个自定义屏
## 幕。

screen about():

    tag menu

    ## 此 use 语句将 game_menu 屏幕包含到了这个屏幕内。子级 vbox 将包含在
    ## game_menu 屏幕的 viewport 内。
    use game_menu(_("关于"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("版本 [config.version!t]\n")

            ## gui.about 通常在 options.rpy 中设置。
            if gui.about:
                text "[gui.about!t]\n"

            text _("引擎：{a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only]\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## 读取和保存屏幕 #####################################################################
##
## 这些屏幕负责让用户保存游戏并能够再次读取。由于它们几乎完全一样，因此这两个屏
## 幕都是以第三个屏幕 file_slots 来实现的。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#save https://doc.renpy.cn/zh-
## CN/screen_special.html#load
init python:
    import re

screen save():

    tag menu

    add "gui/overlay/save_menu.png"
    
    fixed:
        ## 此代码确保输入控件在任意按钮执行前可以获取 enter 事件。
        order_reverse True

        grid gui.file_slot_cols gui.file_slot_rows:
            style_prefix "slot"
            xalign 0.5
            yalign 0.5
            spacing gui.slot_spacing

            for i in range(gui.file_slot_cols * gui.file_slot_rows):

                $ slot = i + 1

                button:
                    action FileAction(slot)
                    background "gui/overlay/save_bg.png"
                    hover_background "gui/overlay/save_bg_on.png"

                    #添加屏幕快照缩略图
                    add FileScreenshot(slot) xysize(260,130) xpos -3 ypos 65
                    
                    vbox:
                        #时间
                        text FileTime(slot, format=_("{#file_time}%Y-%m-%d %H:%M"), empty=_("空存档")):
                            yoffset -13
                            font "SourceHanSerifCN-Medium-6.otf"
                            color "#dff2fc"
                            outlines [(1,"#00000044",0,0)]
                            size 24
                        
                        frame:
                            background None
                            xysize(320,110)
                            xoffset 0
                            yoffset -16
                            #存档描述
                            text FileSaveName(slot):
                                font "SourceHanSerifCN-Medium-6.otf"
                                color "#dff2fc"
                                outlines [(1,"#00000044",0,0)]
                                size 20

                    if len(_last_say_what) >13:
                        action [SetVariable("save_name", re.sub('(\{.*?\})|(\\\w)|\s', '', _last_say_what[:13])+"..."),FileAction(slot) ]
                    elif len(_last_say_what) > 0:
                        action [SetVariable("save_name", re.sub('(\{.*?\})|(\\\w)|\s', '', _last_say_what)),FileAction(slot) ]
                    else:
                        action FileAction(slot)

                    #删除存档
                    imagebutton:
                        xysize(40,94)
                        xpos 260
                        ypos 90
                        idle "gui/button/sl_delete_off.png"
                        hover"gui/button/sl_delete_on.png"
                        action FileDelete(slot)

                    key "save_delete" action FileDelete(slot)
                        

        ## 用于访问其他页面的按钮。
        hbox:
            style_prefix "page"
            xalign 0.5
            ypos 750
            spacing 20

            imagebutton:
                idle "gui/button/save_on_A.png"
                hover "gui/button/save_off_A.png"
                selected_idle "gui/button/save_off_A.png"
                action FilePage("auto")

            imagebutton:
                idle "gui/button/save_on_Q.png"
                hover "gui/button/save_off_Q.png"
                selected_idle "gui/button/save_off_Q.png"
                action FilePage("quick")

            imagebutton:
                idle "gui/button/save_on_1.png"
                hover "gui/button/save_off_1.png"
                selected_idle "gui/button/save_off_1.png"
                action FilePage(1)

            imagebutton:
                idle "gui/button/save_on_2.png"
                hover "gui/button/save_off_2.png"
                selected_idle "gui/button/save_off_2.png"
                action FilePage(2)

            imagebutton:
                idle "gui/button/save_on_3.png"
                hover "gui/button/save_off_3.png"
                selected_idle "gui/button/save_off_3.png"
                action FilePage(3)

            imagebutton:
                idle "gui/button/save_on_4.png"
                hover "gui/button/save_off_4.png"
                selected_idle "gui/button/save_off_4.png"
                action FilePage(4)

            imagebutton:
                idle "gui/button/save_on_5.png"
                hover "gui/button/save_off_5.png"
                selected_idle "gui/button/save_off_5.png"
                action FilePage(5)
            
            imagebutton:
                idle "gui/button/save_on_6.png"
                hover "gui/button/save_off_6.png"
                selected_idle "gui/button/save_off_6.png"
                action FilePage(6)

            imagebutton:
                idle "gui/button/save_on_7.png"
                hover "gui/button/save_off_7.png"
                selected_idle "gui/button/save_off_7.png"
                action FilePage(7)

            imagebutton:
                idle "gui/button/save_on_8.png"
                hover "gui/button/save_off_8.png"
                selected_idle "gui/button/save_off_8.png"
                action FilePage(8)

            imagebutton:
                idle "gui/button/save_on_9.png"
                hover "gui/button/save_off_9.png"
                selected_idle "gui/button/save_off_9.png"
                action FilePage(9)
        
        hbox:
            xalign 0.83
            yalign 0.04
            spacing 20

            imagebutton:
                idle "gui/button/config_off_save.png"
                hover "gui/button/config_off_save.png"
                action ShowMenu('save')

            imagebutton:
                idle "gui/button/config_on_load.png"
                hover "gui/button/config_off_load.png"
                action ShowMenu('load')

        hbox:
            xalign 0.83
            yalign 0.96
            spacing 20
                
            imagebutton:
                idle "gui/button/config_on_title.png"
                hover "gui/button/config_off_title.png"
                action Confirm("是否返回标题界面？", [Show('main_menu'),Play("music", config.main_menu_music)])

            imagebutton:
                idle "gui/button/config_on_quit.png"
                hover "gui/button/config_off_quit.png"
                action Quit(confirm=True)

            imagebutton:
                idle "gui/button/config_on_back.png"
                hover "gui/button/config_off_back.png"
                action Return()



screen load():

    tag menu

    add "gui/overlay/load_menu.png"

    fixed:
        ## 此代码确保输入控件在任意按钮执行前可以获取 enter 事件。
        order_reverse True

        grid gui.file_slot_cols gui.file_slot_rows:
            style_prefix "slot"
            xalign 0.5
            yalign 0.5
            spacing gui.slot_spacing

            for i in range(gui.file_slot_cols * gui.file_slot_rows):

                $ slot = i + 1

                button:
                    action FileAction(slot)
                    background "gui/overlay/load_bg.png"
                    hover_background "gui/overlay/load_bg_on.png"

                    #添加屏幕快照缩略图
                    add FileScreenshot(slot) xysize(260,130) xpos -3 ypos 65
                    
                    vbox:
                        #时间
                        text FileTime(slot, format=_("{#file_time}%Y-%m-%d %H:%M"), empty=_("空存档")):
                            yoffset -13
                            font "SourceHanSerifCN-Medium-6.otf"
                            color "#f18d00"
                            outlines [(1,"#00000044",0,0)]
                            size 24
                        
                        frame:
                            background None
                            xysize(320,110)
                            xoffset 0
                            yoffset -16
                            #存档描述
                            text FileSaveName(slot):
                                font "SourceHanSerifCN-Medium-6.otf"
                                color "#f18d00"
                                outlines [(1,"#00000044",0,0)]
                                size 20

                    #删除存档
                    imagebutton:
                        xysize(40,94)
                        xpos 260
                        ypos 90
                        idle "gui/button/sl_delete_on.png"
                        hover"gui/button/sl_delete_off.png"
                        action FileDelete(slot)

                    key "save_delete" action FileDelete(slot)
                        

        ## 用于访问其他页面的按钮。
        hbox:
            style_prefix "page"
            xalign 0.5
            ypos 750
            spacing 20

            imagebutton:
                idle "gui/button/load_on_A.png"
                hover "gui/button/load_off_A.png"
                selected_idle "gui/button/load_off_A.png"
                action FilePage("auto")

            imagebutton:
                idle "gui/button/load_on_Q.png"
                hover "gui/button/load_off_Q.png"
                selected_idle "gui/button/load_off_Q.png"
                action FilePage("quick")

            imagebutton:
                idle "gui/button/load_on_1.png"
                hover "gui/button/load_off_1.png"
                selected_idle "gui/button/load_off_1.png"
                action FilePage(1)

            imagebutton:
                idle "gui/button/load_on_2.png"
                hover "gui/button/load_off_2.png"
                selected_idle "gui/button/load_off_2.png"
                action FilePage(2)

            imagebutton:
                idle "gui/button/load_on_3.png"
                hover "gui/button/load_off_3.png"
                selected_idle "gui/button/load_off_3.png"
                action FilePage(3)

            imagebutton:
                idle "gui/button/load_on_4.png"
                hover "gui/button/load_off_4.png"
                selected_idle "gui/button/load_off_4.png"
                action FilePage(4)

            imagebutton:
                idle "gui/button/load_on_5.png"
                hover "gui/button/load_off_5.png"
                selected_idle "gui/button/load_off_5.png"
                action FilePage(5)
            
            imagebutton:
                idle "gui/button/load_on_6.png"
                hover "gui/button/load_off_6.png"
                selected_idle "gui/button/load_off_6.png"
                action FilePage(6)

            imagebutton:
                idle "gui/button/load_on_7.png"
                hover "gui/button/load_off_7.png"
                selected_idle "gui/button/load_off_7.png"
                action FilePage(7)

            imagebutton:
                idle "gui/button/load_on_8.png"
                hover "gui/button/load_off_8.png"
                selected_idle "gui/button/load_off_8.png"
                action FilePage(8)

            imagebutton:
                idle "gui/button/load_on_9.png"
                hover "gui/button/load_off_9.png"
                selected_idle "gui/button/load_off_9.png"
                action FilePage(9)
        
        hbox:
            xalign 0.83
            yalign 0.04
            spacing 20

            imagebutton:
                idle "gui/button/config_on_save.png"
                hover "gui/button/config_off_save.png"
                action ShowMenu('save')

            imagebutton:
                idle "gui/button/config_off_load.png"
                hover "gui/button/config_off_load.png"
                action ShowMenu('load')

        hbox:
            xalign 0.83
            yalign 0.96
            spacing 20
                
            imagebutton:
                idle "gui/button/config_on_title.png"
                hover "gui/button/config_off_title.png"
                action Confirm("是否返回标题界面？", [Show('main_menu'),Play("music", config.main_menu_music)])

            imagebutton:
                idle "gui/button/config_on_quit.png"
                hover "gui/button/config_off_quit.png"
                action Quit(confirm=True)

            imagebutton:
                idle "gui/button/config_on_back.png"
                hover "gui/button/config_off_back.png"
                action Return()




# screen file_slots(title):

#     # default page_name_value = FilePageNameInputValue(pattern=_("第 {} 页"), auto=_("自动存档"), quick=_("快速存档"))

#     # use game_menu(title):

#         fixed:

#             ## 此代码确保输入控件在任意按钮执行前可以获取 enter 事件。
#             order_reverse True

#             # ## 页面名称，可以通过单击按钮进行编辑。
#             # button:
#             #     style "page_label"

#             #     key_events True
#             #     xalign 0.5
#             #     action page_name_value.Toggle()

#             #     input:
#             #         style "page_label_text"
#             #         value page_name_value

#             ## 存档位网格。
#             grid gui.file_slot_cols gui.file_slot_rows:
#                 style_prefix "slot"

#                 xalign 0.5
#                 yalign 0.5

#                 spacing gui.slot_spacing

#                 for i in range(gui.file_slot_cols * gui.file_slot_rows):

#                     $ slot = i + 1

#                     button:
#                         action FileAction(slot)

#                         if CurrentScreenName() == "save":
#                             background "gui/overlay/save_bg.png"
#                         else:
#                             background "gui/overlay/load_bg.png"

#                         #添加屏幕快照缩略图
#                         add FileScreenshot(slot) xysize(260,130) xoffset 10 yoffset 80
                        
#                         vbox:
#                             #时间
#                             text FileTime(slot, format=_("{#file_time}%Y-%m-%d %H:%M"), empty=_("空存档")):
#                                 font "SourceHanSerifCN-Medium-6.otf"
#                                 color "#dff2fc"
#                                 outlines [(2,"#00000088",0,0)]
#                                 size 32
                            
#                             frame:
#                                 background None
#                                 xysize(210,110)
#                                 xoffset 230
#                                 yoffset 20
#                                 #存档描述
#                                 text FileSaveName(slot):
#                                     size 25

#                         #删除存档
#                         if CurrentScreenName() == "save":
#                             imagebutton:
#                                 xysize(40,94)
#                                 align((1.0, 0.9))
#                                 idle "gui/button/sl_delete_on.png"
#                                 hover"gui/button/sl_delete_off.png"
#                                 action FileDelete(slot)
#                         else:
#                             imagebutton:
#                                 xysize(40,94)
#                                 align((1.0, 0.9))
#                                 idle "gui/button/sl_delete_off.png"
#                                 hover"gui/button/sl_delete_on.png"
#                                 action FileDelete(slot)
                            
#                         #添加存档描述，正则表达式，该语句只可用于存档界面
#                         if CurrentScreenName() == "save":
#                             if len(_last_say_what) >15:
#                                 action [SetVariable("save_name", re.sub('(\{.*?\})|(\\\w)|\s', '', _last_say_what[:15])+"..."),FileAction(slot) ]
#                             elif len(_last_say_what) > 0:
#                                 action [SetVariable("save_name", re.sub('(\{.*?\})|(\\\w)|\s', '', _last_say_what)),FileAction(slot) ]
#                             else:
#                                 action FileAction(slot)

#                         key "save_delete" action FileDelete(slot)

#             ## 用于访问其他页面的按钮。
#             vbox:
#                 style_prefix "page"

#                 xalign 0.5
#                 yalign 1.0

#                 hbox:
#                     xalign 0.5

#                     spacing gui.page_spacing

#                     textbutton _("<") action FilePagePrevious()
#                     key "save_page_prev" action FilePagePrevious()

#                     if config.has_autosave:
#                         textbutton _("{#auto_page}A") action FilePage("auto")

#                     if config.has_quicksave:
#                         textbutton _("{#quick_page}Q") action FilePage("quick")

#                     ## range(1, 10) 给出 1 到 9 之间的数字。
#                     for page in range(1, 10):
#                         textbutton "[page]" action FilePage(page)

#                     textbutton _(">") action FilePageNext()
#                     key "save_page_next" action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 63
    ypadding 4

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## SYSTEM设置屏幕 ########################################################################
##
## 点击设置默认进入系统设置界面。
screen preferences():

    tag menu
    
    add "gui/overlay/config_menu.png"
    ##切换用按钮
    hbox:
        xalign 0.83
        yalign 0.04
        spacing 20

        imagebutton:
            idle "gui/button/config_off_system.png"
            hover "gui/button/config_off_system.png"
            action ShowMenu('preferences')

        imagebutton:
            idle "gui/button/config_on_text.png"
            hover "gui/button/config_off_text.png"
            action ShowMenu('text')

        # imagebutton:
        #     idle "gui/button/config_on_sound.png"
        #     hover "gui/button/config_off_sound.png"
        #     action ShowMenu('sound')

        imagebutton:
            idle "gui/button/config_on_voice.png"
            hover "gui/button/config_off_voice.png"
            action ShowMenu('voice')

    hbox:
        xalign 0.83
        yalign 0.96
        spacing 20

        imagebutton:
            idle "gui/button/config_on_reset.png"
            hover "gui/button/config_off_reset.png"
            action Confirm("是否重置所有设置？", Function(func_reset,True))
            
        imagebutton:
            idle "gui/button/config_on_title.png"
            hover "gui/button/config_off_title.png"
            action Confirm("是否返回标题界面？", [Show('main_menu'),Play("music", config.main_menu_music)])

        imagebutton:
            idle "gui/button/config_on_quit.png"
            hover "gui/button/config_off_quit.png"
            action Quit(confirm=True)

        imagebutton:
            idle "gui/button/config_on_back.png"
            hover "gui/button/config_off_back.png"
            action Return()

    vbox:
        xpos 200
        ypos 160
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}显示模式{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]

        hbox:
            spacing 15
            ## 窗口状态下
            if preferences.fullscreen == False:
                imagebutton:
                    idle "gui/button/button_on_fullsc.png"
                    hover "gui/button/button_off_fullsc.png"
                    action Preference("display", "fullscreen")
                imagebutton:
                    idle "gui/button/button_off_windowed.png"
                    action Preference("display", "window")
            ## 全屏状态下
            else:
                imagebutton:
                    idle "gui/button/button_off_fullsc.png"
                    action Preference("display", "fullscreen")
                imagebutton:
                    idle "gui/button/button_on_windowed.png"
                    hover "gui/button/button_off_windowed.png"
                    action Preference("display", "window")

    vbox:
        xpos 200
        ypos 300
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}转场动画显示{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        hbox:
            spacing 20 
            ## 显示所有转场
            if preferences.transitions == 2:
                imagebutton:
                    idle "gui/button/button_off_yes.png"
                    action Preference("transitions", "all")
                imagebutton:
                    idle "gui/button/button_on_no.png"
                    hover "gui/button/button_off_no.png"
                    action Preference("transitions", "none")
            ## 忽略所有转场
            if preferences.transitions == 0:
                imagebutton:
                    idle "gui/button/button_on_yes.png"
                    hover "gui/button/button_off_yes.png"
                    action Preference("transitions", "all")
                imagebutton:
                    idle "gui/button/button_off_no.png"
                    action Preference("transitions", "none")
    
    vbox:
        xpos 200
        ypos 440
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}确认对话框显示{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        hbox:
            spacing 20 
            ## 关闭确认对话框
            if persistent.confirmation_dialog == True:
                imagebutton:
                    idle "gui/button/button_off_yes.png"
                    action SetVariable("persistent.confirmation_dialog", True) 
                imagebutton:
                    idle "gui/button/button_on_no.png"
                    hover "gui/button/button_off_no.png"
                    action SetVariable("persistent.confirmation_dialog", False)
            ## 开启确认对话框
            else:
                imagebutton:
                    idle "gui/button/button_on_yes.png"
                    hover "gui/button/button_off_yes.png"
                    action SetVariable("persistent.confirmation_dialog", True) 
                imagebutton:
                    idle "gui/button/button_off_no.png"
                    action SetVariable("persistent.confirmation_dialog", False)


    if persistent.confirmation_dialog == True:
        vbox:
            xpos 200
            ypos 580
            spacing 10
            hbox:
                spacing 10
                add "gui/overlay/config_special.png"
                text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}自动移动光标{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
            hbox:
                spacing 20 
                ## 允许鼠标自动移动
                if preferences.mouse_move == True:
                    imagebutton:
                        idle "gui/button/button_off_yes.png"
                        action Preference("automatic move", "enable") 
                    imagebutton:
                        idle "gui/button/button_on_no.png"
                        hover "gui/button/button_off_no.png"
                        action Preference("automatic move", "disable")
                ## 禁止鼠标自动移动
                else:
                    imagebutton:
                        idle "gui/button/button_on_yes.png"
                        hover "gui/button/button_off_yes.png"
                        action Preference("automatic move", "enable") 
                    imagebutton:
                        idle "gui/button/button_off_no.png"
                        action Preference("automatic move", "disable")
    
    vbox:
        xpos 850
        ypos 160
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}已读文本变色{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        hbox:
            spacing 20 
            ## 已读文本不变色
            if persistent.text_color_change == True:
                imagebutton:
                    idle "gui/button/button_off_yes.png"
                    action SetVariable("persistent.text_color_change", True) 
                imagebutton:
                    idle "gui/button/button_on_no.png"
                    hover "gui/button/button_off_no.png"
                    action SetVariable("persistent.text_color_change", False)
            ## 已读文本变色
            else:
                imagebutton:
                    idle "gui/button/button_on_yes.png"
                    hover "gui/button/button_off_yes.png"
                    action SetVariable("persistent.text_color_change", True) 
                imagebutton:
                    idle "gui/button/button_off_no.png"
                    action SetVariable("persistent.text_color_change", False)

    vbox:
        xpos 850
        ypos 300
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}自动模式等待语音播放完毕{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        hbox:
            spacing 20 
            ## 等待语音播放完毕
            if preferences.wait_voice ==True:
                imagebutton:
                    idle "gui/button/button_off_yes.png"
                    action Preference("wait for voice", "enable")
                imagebutton:
                    idle "gui/button/button_on_no.png"
                    hover "gui/button/button_off_no.png"
                    action Preference("wait for voice", "disable") 
            ## 不等待语音播放完毕
            else:
                imagebutton:
                    idle "gui/button/button_on_yes.png"
                    hover "gui/button/button_off_yes.png"
                    action Preference("wait for voice", "enable")
                imagebutton:
                    idle "gui/button/button_off_no.png"
                    action Preference("wait for voice", "disable") 

    vbox:
        xpos 850
        ypos 440
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}翻页时停止播放当前语音{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        hbox:
            spacing 20 
            ## 语音中断
            if preferences.voice_sustain ==False:
                imagebutton:
                    idle "gui/button/button_off_yes.png"
                    action Preference("voice sustain", "disable") 
                imagebutton:
                    idle "gui/button/button_on_no.png"
                    hover "gui/button/button_off_no.png"
                    action Preference("voice sustain", "enable")
            ## 不中断
            else:
                imagebutton:
                    idle "gui/button/button_on_yes.png"
                    hover "gui/button/button_off_yes.png"
                    action Preference("voice sustain", "disable") 
                imagebutton:
                    idle "gui/button/button_off_no.png"
                    action Preference("voice sustain", "enable")
    
    vbox:
        xpos 850
        ypos 580
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}允许快进未读文本{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        hbox:
            spacing 20 
            ## 仅已读文本
            if preferences.skip_unseen == True:
                imagebutton:
                    idle "gui/button/button_off_yes.png"
                    action Preference("skip", "all")
                imagebutton:
                    idle "gui/button/button_on_no.png"
                    hover "gui/button/button_off_no.png"
                    action Preference("skip", "seen")
            ## 全部
            else:
                imagebutton:
                    idle "gui/button/button_on_yes.png"
                    hover "gui/button/button_off_yes.png"
                    action Preference("skip", "all")
                imagebutton:
                    idle "gui/button/button_off_no.png"
                    action Preference("skip", "seen")



## 文本预览用屏幕1
screen speed_preview1():
    tag preview
    frame:
        xpos 190
        ypos 600
        xysize(500, 120)
        background im.Alpha("gui/overlay/textbox_preview.png", persistent.textbox_alpha)

        text "这是文本播放时以及\n自动模式的效果展示。" :
            xalign .1 
            outlines [(2,"#00000088",0,0)]
            slow_cps persistent.text_displayspeed


## TEXT设置屏幕 ########################################################################
##
## 文本设置，从系统设置切换。
screen text():

    tag menu
    
    add "gui/overlay/config_menu.png"

    timer 0.1:
        action Show("speed_preview1")
    if persistent.text_displayspeed == 0:
        timer (preferences.afm_time):
            repeat (persistent.text_displayspeed == 0)
            action [Hide('speed_preview1'), Show("speed_preview1")]
    else:
        timer ((20/persistent.text_displayspeed)+preferences.afm_time):
            repeat (persistent.text_displayspeed != 0)
            action [Hide('speed_preview1'), Show("speed_preview1")]

    frame:
        xpos 190
        ypos 600
        background Solid("#FFFFFF00", xsize = 500, ysize = 120)

    ##切换用按钮
    hbox:
        xalign 0.83
        yalign 0.04
        spacing 20

        imagebutton:
            idle "gui/button/config_on_system.png"
            hover "gui/button/config_off_system.png"
            action [Hide("speed_preview1"), ShowMenu('preferences')]

        imagebutton:
            idle "gui/button/config_off_text.png"
            hover "gui/button/config_off_text.png"
            action [Hide("speed_preview1"), ShowMenu('text')]

        # imagebutton:
        #     idle "gui/button/config_on_sound.png"
        #     hover "gui/button/config_off_sound.png"
        #     action [Hide("speed_preview1"), ShowMenu('sound')]

        imagebutton:
            idle "gui/button/config_on_voice.png"
            hover "gui/button/config_off_voice.png"
            action [Hide("speed_preview1"), ShowMenu('voice')]

    hbox:
        xalign 0.83
        yalign 0.96
        spacing 20

        imagebutton:
            idle "gui/button/config_on_reset.png"
            hover "gui/button/config_off_reset.png"
            action [Hide("speed_preview1"), Confirm("是否重置所有设置？", [Hide("speed_preview1"), Function(func_reset,True)])]

        imagebutton:
            idle "gui/button/config_on_title.png"
            hover "gui/button/config_off_title.png"
            action [Hide("speed_preview1"), Confirm("是否返回标题界面？", [Hide("speed_preview1"), Play("music", config.main_menu_music), Show('main_menu')])]

        imagebutton:
            idle "gui/button/config_on_quit.png"
            hover "gui/button/config_off_quit.png"
            action Quit(confirm=True)

        imagebutton:
            idle "gui/button/config_on_back.png"
            hover "gui/button/config_off_back.png"
            action [Hide("speed_preview1"), Return()]

    vbox:
        xpos 200
        ypos 160
        spacing 10

        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}文本显示速度{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
            
        hbox:
            spacing 5
            bar:
                value VariableValue("persistent.text_displayspeed",range=100)
                xsize 440
                right_bar "gui/slider/slider_horizontal_off.png"
                left_bar "gui/slider/slider_horizontal_on.png"
                thumb "gui/slider/thumb_horizontal_on.png"
            frame:
                background "gui/slider/slider_background.png"
                if persistent.text_displayspeed == 0:
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}瞬间{/color}{/size}{/font}" xoffset 5 yoffset -16
                else:
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[persistent.text_displayspeed]{/color}{/size}{/font}" xoffset 5 yoffset -16

    vbox:
        xpos 200
        ypos 300      
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}自动模式文本等待时间{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        hbox:
            spacing 5
            bar:
                #value Preference("auto-forward time",range=30)
                value VariableValue("persistent.text_autospeed",range=100)                
                xsize 440
                right_bar "gui/slider/slider_horizontal_off.png"
                left_bar "gui/slider/slider_horizontal_on.png"
                thumb "gui/slider/thumb_horizontal_on.png"
            frame:
                background "gui/slider/slider_background.png"
                $ preferences.afm_time = 0.5 + persistent.text_autospeed/20
                text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[persistent.text_autospeed]{/color}{/size}{/font}" xoffset 5 yoffset -16


    vbox: 
        xpos 200
        ypos 440
        spacing 10

        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}对话框不透明度{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
            
        hbox:
            spacing 5
            bar:
                value FieldValue(persistent, "textbox_alpha", range=1.0, style="slider")
                xsize 440
                right_bar "gui/slider/slider_horizontal_off.png"
                left_bar "gui/slider/slider_horizontal_on.png"
                thumb "gui/slider/thumb_horizontal_on.png"
            frame:
                background "gui/slider/slider_background.png"
                $ textalpha=int(persistent.textbox_alpha*100)
                text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[textalpha]{/color}{/size}{/font}" xoffset 5 yoffset -16

    # vbox:
    #     xpos 200
    #     ypos 580
    #     spacing 10
    #     hbox:
    #         spacing 10
    #         add "gui/overlay/config_special.png"
    #         text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}文本显示预览{/size}{/font}" color "#dff2fc" 
    #     hbox:
    #         spacing 20 
    #         ## 默认模式
    #         if text_read:
    #             imagebutton:
    #                 idle "gui/button/button_off_readmode.png"
    #                 action [SetVariable("text_read", True)]
    #             imagebutton:
    #                 idle "gui/button/button_on_automode.png"
    #                 hover "gui/button/button_off_automode.png"
    #                 action [SetVariable("text_read", False)]
    #         ## 自动模式
    #         else:
    #             imagebutton:
    #                 idle "gui/button/button_on_readmode.png"
    #                 hover "gui/button/button_off_readmode.png"
    #                 action [SetVariable("text_read", True)]
    #             imagebutton:
    #                 idle "gui/button/button_off_automode.png"
    #                 action [SetVariable("text_read", False)]
        
    vbox:
        xpos 850
        ypos 160
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}全局音量设置{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
                 
        vbox:
            hbox:
                spacing 20
                bar:
                    value Preference("main volume")
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ main_volume = int(preferences.get_mixer("main")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[main_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16

    vbox:
        xpos 850
        ypos 300
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}背景音乐音量设置{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
        vbox:
            hbox:
                spacing 20
                bar:
                    value Preference("music volume")
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ music_volume = int(preferences.get_mixer("music")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[music_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16

    vbox:
        xpos 850
        ypos 440
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}音效音量设置{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
            imagebutton:
                idle "gui/overlay/config_sound_on.png"
                hover "gui/overlay/config_sound_off.png"
                action Play("audio", "audio/BGS/RingBell.ogg")

        vbox:
            hbox:
                spacing 20
                bar:
                    value Preference("sound volume")
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ sound_volume = int(preferences.get_mixer("sfx")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[sound_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16
    
    vbox:
        xpos 850
        ypos 580
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}语音音量设置{/size}{/font}" color "#dff2fc" outlines [(2,"#00000088",0,0)]
            imagebutton:
                idle "gui/overlay/config_sound_on.png"
                hover "gui/overlay/config_sound_off.png"
                action Play("voice", "audio/BGS/RingBell.ogg")
        vbox:
            hbox:
                spacing 20
                bar:
                    value Preference("voice volume")
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ voice_volume=int(preferences.get_mixer("voice")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[voice_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16

    


# ## SOUND设置屏幕 ########################################################################
# ##
# ## 系统音量设置，从系统设置切换。
# screen sound():

#     tag menu
    
#     add "gui/overlay/config_menu.png"
#     ##切换用按钮
#     hbox:
#         xalign 0.83
#         yalign 0.04
#         spacing 20

#         imagebutton:
#             idle "gui/button/config_on_system.png"
#             hover "gui/button/config_off_system.png"
#             action ShowMenu('preferences')

#         imagebutton:
#             idle "gui/button/config_on_text.png"
#             hover "gui/button/config_off_text.png"
#             action ShowMenu('text')

#         imagebutton:
#             idle "gui/button/config_off_sound.png"
#             hover "gui/button/config_off_sound.png"
#             action ShowMenu('sound')

#         imagebutton:
#             idle "gui/button/config_on_voice.png"
#             hover "gui/button/config_off_voice.png"
#             action ShowMenu('voice')

#     hbox:
#         xalign 0.83
#         yalign 0.96
#         spacing 20

#         imagebutton:
#             idle "gui/button/config_on_reset.png"
#             hover "gui/button/config_off_reset.png"
#             action Confirm("是否重置所有设置？", Function(func_reset,True))
            

#         imagebutton:
#             idle "gui/button/config_on_title.png"
#             hover "gui/button/config_off_title.png"
#             action Confirm("是否返回标题界面？", Show('main_menu'))

#         imagebutton:
#             idle "gui/button/config_on_quit.png"
#             hover "gui/button/config_off_quit.png"
#             action Quit(confirm=True)

#         imagebutton:
#             idle "gui/button/config_on_back.png"
#             hover "gui/button/config_off_back.png"
#             action Return()
init python:
    ## 判断字典存不存在，不存在则创建
    if not hasattr(persistent, '_character_volume'):
        persistent._character_volume = {}  
    
    ## 判断字典的 key 存不存在，不存在创建 key 并赐值
    if 'bxh' not in persistent._character_volume:
        persistent._character_volume['bxh'] = 1.0  
    if 'djf' not in persistent._character_volume:
        persistent._character_volume['djf'] = 1.0  
    if 'gmr' not in persistent._character_volume:
        persistent._character_volume['gmr'] = 1.0  
    if 'others' not in persistent._character_volume:
        persistent._character_volume['others'] = 1.0  

## VOICE设置屏幕 ########################################################################
##
## 角色音量设置，从系统设置切换。
screen voice():

    tag menu
    
    add "gui/overlay/config_menu.png"
    ##切换用按钮
    hbox:
        xalign 0.83
        yalign 0.04
        spacing 20

        imagebutton:
            idle "gui/button/config_on_system.png"
            hover "gui/button/config_off_system.png"
            action ShowMenu('preferences')

        imagebutton:
            idle "gui/button/config_on_text.png"
            hover "gui/button/config_off_text.png"
            action ShowMenu('text')

        # imagebutton:
        #     idle "gui/button/config_on_sound.png"
        #     hover "gui/button/config_off_sound.png"
        #     action ShowMenu('sound')

        imagebutton:
            idle "gui/button/config_off_voice.png"
            hover "gui/button/config_off_voice.png"
            action ShowMenu('voice')

    hbox:
        xalign 0.83
        yalign 0.96
        spacing 20

        imagebutton:
            idle "gui/button/config_on_reset.png"
            hover "gui/button/config_off_reset.png"
            action Confirm("是否重置所有设置？", Function(func_reset,True))
            

        imagebutton:
            idle "gui/button/config_on_title.png"
            hover "gui/button/config_off_title.png"
            action Confirm("是否返回标题界面？", [Show('main_menu'),Play("music", config.main_menu_music)])

        imagebutton:
            idle "gui/button/config_on_quit.png"
            hover "gui/button/config_off_quit.png"
            action Quit(confirm=True)

        imagebutton:
            idle "gui/button/config_on_back.png"
            hover "gui/button/config_off_back.png"
            action Return()

 

    vbox:
        xpos 200
        ypos 200
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}包馨荷{/size}{/font}" color "#d7ee05" outlines [(2,"#00000088",0,0)]
        vbox:
            hbox:
                spacing 20
                bar:
                    value DictValue(dict=persistent._character_volume ,key="bxh", range=1.0)
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ bxh_voice_volume = int(GetCharacterVolume("bxh")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[bxh_voice_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16

    vbox:
        xpos 200
        ypos 520
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}杜绛枫{/size}{/font}" color "#da21bb" outlines [(2,"#00000088",0,0)]
        vbox:
            hbox:
                spacing 20
                bar:
                    value DictValue(dict=persistent._character_volume ,key="djf", range=1.0)
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ djf_voice_volume = int(GetCharacterVolume("djf")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[djf_voice_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16
    
    vbox:
        xpos 850
        ypos 200
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}郭茉渃{/size}{/font}" color "#ffffe6" outlines [(2,"#00000088",0,0)]
        vbox:
            hbox:
                spacing 20
                bar:
                    value DictValue(dict=persistent._character_volume ,key="gmr", range=1.0)
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ gmr_voice_volume = int(GetCharacterVolume("gmr")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[gmr_voice_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16

    vbox:
        xpos 850
        ypos 520
        spacing 10
        hbox:
            spacing 10
            add "gui/overlay/config_special.png"
            text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}其他{/size}{/font}" color "#7c0029" outlines [(2,"#00000088",0,0)]
        vbox:
            hbox:
                spacing 20
                bar:
                    value DictValue(dict=persistent._character_volume ,key="others", range=1.0)
                    xsize 440
                    right_bar "gui/slider/slider_horizontal_off.png"
                    left_bar "gui/slider/slider_horizontal_on.png"
                    thumb "gui/slider/thumb_horizontal_on.png"
                frame:
                    background "gui/slider/slider_background.png"
                    $ others_voice_volume = int(GetCharacterVolume("others")*100)
                    text "{font=SourceHanSerifCN-Medium-6.otf}{size=32}{color=#dff2fc}[others_voice_volume]{/color}{/size}{/font}" xoffset 5 yoffset -16
    





## 设置屏幕 ########################################################################
##
## 设置屏幕允许用户配置游戏，使其更适合自己。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#preferences

# screen preferences():

#     tag menu

#     use game_menu(_("设置"), scroll="viewport"):

#         vbox:

#             hbox:
#                 box_wrap True

#                 if renpy.variant("pc") or renpy.variant("web"):

#                     vbox:
#                         style_prefix "radio"
#                         label _("显示")
#                         textbutton _("窗口") action Preference("display", "window")
#                         textbutton _("全屏") action Preference("display", "fullscreen")

#                 vbox:
#                     style_prefix "check"
#                     label _("快进")
#                     textbutton _("未读文本") action Preference("skip", "toggle")
#                     textbutton _("选项后继续") action Preference("after choices", "toggle")
#                     textbutton _("忽略转场") action InvertSelected(Preference("transitions", "toggle"))

#                 ## 可在此处添加 radio_pref 或 check_pref 类型的额外 vbox，以添加
#                 ## 额外的创建者定义的偏好设置。

#             null height (4 * gui.pref_spacing)

#             hbox:
#                 style_prefix "slider"
#                 box_wrap True

#                 vbox:

#                     label _("文字速度")

#                     bar value Preference("text speed")

#                     label _("自动前进时间")

#                     bar value Preference("auto-forward time")

#                 vbox:

#                     if config.has_music:
#                         label _("音乐音量")

#                         hbox:
#                             bar value Preference("music volume")

#                     if config.has_sound:

#                         label _("音效音量")

#                         hbox:
#                             bar value Preference("sound volume")

#                             if config.sample_sound:
#                                 textbutton _("测试") action Play("sound", config.sample_sound)


#                     if config.has_voice:
#                         label _("语音音量")

#                         hbox:
#                             bar value Preference("voice volume")

#                             if config.sample_voice:
#                                 textbutton _("测试") action Play("voice", config.sample_voice)

#                     if config.has_music or config.has_sound or config.has_voice:
#                         null height gui.pref_spacing

#                         textbutton _("全部静音"):
#                             action Preference("all mute", "toggle")
#                             style "mute_all_button"


# style pref_label is gui_label
# style pref_label_text is gui_label_text
# style pref_vbox is vbox

# style radio_label is pref_label
# style radio_label_text is pref_label_text
# style radio_button is gui_button
# style radio_button_text is gui_button_text
# style radio_vbox is pref_vbox

# style check_label is pref_label
# style check_label_text is pref_label_text
# style check_button is gui_button
# style check_button_text is gui_button_text
# style check_vbox is pref_vbox

# style slider_label is pref_label
# style slider_label_text is pref_label_text
# style slider_slider is gui_slider
# style slider_button is gui_button
# style slider_button_text is gui_button_text
# style slider_pref_vbox is pref_vbox

# style mute_all_button is check_button
# style mute_all_button_text is check_button_text

# style pref_label:
#     top_margin gui.pref_spacing
#     bottom_margin 3

# style pref_label_text:
#     yalign 1.0

# style pref_vbox:
#     xsize 282

# style radio_vbox:
#     spacing gui.pref_button_spacing

# style radio_button:
#     properties gui.button_properties("radio_button")
#     foreground "gui/button/radio_[prefix_]foreground.png"

# style radio_button_text:
#     properties gui.text_properties("radio_button")

# style check_vbox:
#     spacing gui.pref_button_spacing

# style check_button:
#     properties gui.button_properties("check_button")
#     foreground "gui/button/check_[prefix_]foreground.png"

# style check_button_text:
#     properties gui.text_properties("check_button")

# style slider_slider:
#     xsize 438

# style slider_button:
#     properties gui.button_properties("slider_button")
#     yalign 0.5
#     left_margin 13

# style slider_button_text:
#     properties gui.text_properties("slider_button")

# style slider_vbox:
#     xsize 563

# 滚轮下滑关闭历史记录
init python:
    class MyAdjustment(renpy.display.behavior.Adjustment):
        def change(self, value, end_animation=True):
            if value > self._range and self._value == self._range:
                # 返回游戏界面
                return Return()
            else:
                # 其他情况，正常执行
                return renpy.display.behavior.Adjustment.change(self, value, end_animation)
# 理论上这里的range应该修改为我们需要的范围，但不做修改也不会有问题
default history_bar_pos = MyAdjustment(range = 100,changed =None,adjustable=True)

## 历史屏幕 ########################################################################
##
## 这是一个向用户显示对话历史的屏幕。虽然此屏幕没有什么特别之处，但它必须访问储
## 存在 _history_list 中的对话历史记录。
##
## https://doc.renpy.cn/zh-CN/history.html

screen history():

    tag menu

    ## 避免预缓存此屏幕，因为它可能非常大。
    predict False

    add "gui/overlay/history_menu.png"
    frame:
        style "history_frame_style"
        frame:
            style "history_window_frame_style"
            vpgrid id "history_list":
                #行数
                cols 1
                #视口初始垂直偏移量
                yinitial 1.0
                mousewheel True
                draggable True
                pagekeys True
                side_xfill True
                yadjustment history_bar_pos

                for h in _history_list:
                    
                    window:
                        background None            
                        ysize 165
                        ## 此代码可确保如果 history_height 为 None 时仍可正常显示条目。
                        # has fixed:
                        #     yfit True
                        hbox:   
                            vbox:
                                spacing 10
                                # 跳转按钮
                                imagebutton:
                                    idle "gui/button/history_on_jump.png"
                                    hover "gui/button/history_off_jump.png"
                                    action Confirm("是否跳转到该处？",yes=RollbackToIdentifier(h.rollback_identifier), no=None, confirm_selected=False)
                                if h.voice.filename:
                                    imagebutton:
                                        idle "gui/button/history_on_voice.png"
                                        hover "gui/button/history_off_voice.png"
                                        action Play('voice', h.voice.filename)
                            vbox:
                                if h.who:
                                    label h.who:
                                        style "history_name"
                                        substitute False
                                        ## 从 Character 对象中获取叙述角色的文字颜色，如果设置了
                                        ## 的话。
                                        if "color" in h.who_args:
                                            text_color h.who_args["color"]

                                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                                text what:
                                    style "history_text"
                                    outlines [(1,"#00000088",0,0)]
                                    substitute False

                if not _history_list:
                    label _("尚无对话历史记录。")
    vbox:
        yalign 0.5
        xpos 1400
        spacing 10

        imagebutton:
            idle "gui/slider/up_vertical_on.png"
            hover "gui/slider/up_vertical_off.png"
            action Function(history_bar_pos.change,0)

        # 滚动条
        vbar:
            xsize 32
            ysize 600
            bottom_bar "gui/slider/slider_vertical_off.png"
            top_bar "gui/slider/slider_vertical_on.png"
            thumb "gui/slider/thumb_vertical_on.png"
            value YScrollValue("history_list")
        
        imagebutton:
            idle "gui/slider/down_vertical_on.png"
            hover "gui/slider/down_vertical_off.png"
            # 历史记录最大块数乘高度
            action Function(history_bar_pos.change,config.history_length*200)

    # 返回按钮
    imagebutton:
        align (0.95, 0.95)
        idle "gui/button/config_on_back.png"
        hover "gui/button/config_off_back.png"
        action Return()

    if len(_history_list)<4:
        key "mousedown_5" action Return()

    

#新添加样式  
style history_frame_style:
    left_padding 200 #左边距
    right_padding 200 #右边距

style history_window_frame_style:
    top_padding 140 #顶部边距
    bottom_padding 100 #底部边距
    xfill True


## 此代码决定了允许在历史记录屏幕上显示哪些标签。

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## 帮助屏幕 ########################################################################
##
## 提供有关键盘和鼠标映射信息的屏幕。它使用其它屏幕（keyboard_help、mouse_help
## 和 gamepad_help）来显示实际的帮助内容。

#screen help():

#    tag menu

#    default device = "keyboard"

#    use game_menu(_("帮助"), scroll="viewport"):

#        style_prefix "help"

#        vbox:
#            spacing 19

#            hbox:

#                textbutton _("键盘") action SetScreenVariable("device", "keyboard")
#                textbutton _("鼠标") action SetScreenVariable("device", "mouse")

#                if GamepadExists():
#                    textbutton _("手柄") action SetScreenVariable("device", "gamepad")

#            if device == "keyboard":
#                use keyboard_help
#            elif device == "mouse":
#                use mouse_help
#            elif device == "gamepad":
#                use gamepad_help


#screen keyboard_help():

#    hbox:
#        label _("回车")
#        text _("推进对话并激活界面。")

    # hbox:
    #     label _("空格")
    #     text _("在没有选择的情况下推进对话。")

    # hbox:
    #     label _("方向键")
    #     text _("导航界面。")

    # hbox:
    #     label _("Esc")
    #     text _("访问游戏菜单。")

    # hbox:
    #     label _("键盘")
    #     text _("按住时快进对话。")

    # hbox:
    #     label _("Tab")
    #     text _("切换对话快进。")

    # hbox:
    #     label _("上一页")
    #     text _("回退至先前的对话。")

    # hbox:
    #     label _("下一页")
    #     text _("向前至后来的对话。")

    # hbox:
    #     label "H"
    #     text _("隐藏用户界面。")

    # hbox:
    #     label "S"
    #     text _("截图。")

    # hbox:
    #     label "V"
    #     text _("切换辅助{a=https://doc.renpy.cn/zh-CN/self_voicing.html}机器朗读{/a}。")

    # hbox:
    #     label "Shift+A"
    #     text _("打开无障碍菜单。")


# screen mouse_help():

#     hbox:
#         label _("左键点击")
#         text _("推进对话并激活界面。")

#     hbox:
#         label _("中键点击")
#         text _("隐藏用户界面。")

#     hbox:
#         label _("右键点击")
#         text _("访问游戏菜单。")

#     hbox:
#         label _("鼠标滚轮上")
#         text _("回退至先前的对话。")

#     hbox:
#         label _("鼠标滚轮下")
#         text _("向前至后来的对话。")


# screen gamepad_help():

#     hbox:
#         label _("右扳机键\nA/底键")
#         text _("推进对话并激活界面。")

#     hbox:
#         label _("左扳机键\n左肩键")
#         text _("回退至先前的对话。")

#     hbox:
#         label _("右肩键")
#         text _("向前至后来的对话。")

#     hbox:
#         label _("十字键，摇杆")
#         text _("导航界面。")

#     hbox:
#         label _("开始，向导，B/右键")
#         text _("访问游戏菜单。")

#     hbox:
#         label _("Y/顶键")
#         text _("隐藏用户界面。")

#     textbutton _("校准") action GamepadCalibrate()


# style help_button is gui_button
# style help_button_text is gui_button_text
# style help_label is gui_label
# style help_label_text is gui_label_text
# style help_text is gui_text

# style help_button:
#     properties gui.button_properties("help_button")
#     xmargin 10

# style help_button_text:
#     properties gui.text_properties("help_button")

# style help_label:
#     xsize 313
#     right_padding 25

# style help_label_text:
#     size gui.text_size
#     xalign 1.0
#     textalign 1.0

###CG、BGM解锁条件设置##
#音乐列表
init python:
    #淡入淡出
    mr = MusicRoom(fadein = 1.0 , fadeout = 1.0)
    #音乐列表，第一个用于主界面bgm，设为默认解锁
    mr.add("audio/BGM/桜吹雪の誓い_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/Brand_New_Day_のる.ogg", always_unlocked = True)
    mr.add("audio/BGM/Close_Love_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/Embers_of_a_Vanishing_Sky_MFP(Marron Fields Production).ogg", always_unlocked = True)
    mr.add("audio/BGM/Fighter's_Edge_gooset.ogg", always_unlocked = True)
    mr.add("audio/BGM/Overcome_のる.ogg", always_unlocked = True)
    mr.add("audio/BGM/Umbra_Protocol_松浦洋介.ogg", always_unlocked = True)
    mr.add("audio/BGM/Under_the_Blue_Fizz_松浦洋介.ogg", always_unlocked = True)
    mr.add("audio/BGM/You_Were_the_Last_Light_松浦洋介.ogg", always_unlocked = True)
    mr.add("audio/BGM/Zen_yuhei komatsu.ogg", always_unlocked = True)
    mr.add("audio/BGM/あくる日のワルツ_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/あたたかな雪_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/あの空に向かって_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/いつものカフェで待ち合わせ_秦暁.ogg", always_unlocked = True)
    mr.add("audio/BGM/かつての聖域_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/ほのぼのいい天気_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/タタリ_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/別れの季節_alaki paca.ogg", always_unlocked = True)
    mr.add("audio/BGM/君影草_すもち.ogg", always_unlocked = True)
    mr.add("audio/BGM/夢の中を泳ぐ魚_ゆうきわたる.ogg", always_unlocked = True)
    mr.add("audio/BGM/星空の導き_alaki paca.ogg", always_unlocked = True)
    mr.add("audio/BGM/晴れやかな日の午後に_しんさんわーくす.ogg", always_unlocked = True)
    mr.add("audio/BGM/暗闇を駆け抜けろ！_alaki paca.ogg", always_unlocked = True)
    mr.add("audio/BGM/桜が散る時_yuhei komatsu.ogg", always_unlocked = True) 
    mr.add("audio/BGM/沈みゆく体、浮かぶ意識_alaki paca.ogg", always_unlocked = True)
    mr.add("audio/BGM/祭りの夜_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/言霊_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/路地裏ファンタジー_yuhei komatsu.ogg", always_unlocked = True)
    mr.add("audio/BGM/迫る闇_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/陰謀論_ゆうり(from Yuli Audio Craft).ogg", always_unlocked = True)
    mr.add("audio/BGM/雪、吹き乱れて(Snow,blizzarding)_蒲鉾さちこ.ogg", always_unlocked = True)


    #更多音乐请自行添加
#CG列表
init python:

    g = Gallery()

    g.button("bg")#类似于标签
    g.image("images/test.png")#真正的图片
    g.unlock_image("images/test.png")#差分

    g.button("cg")
    g.condition("persistent.unlock_1")#解锁限制
    #使用方法：
    #脚本内添加 $ persisitent.unlock_1 = True
    g.image("images/test.png")

    #未解锁
    g.button("unlock")

    #更多图像请自行添加
    #图像切换使用的转场。
    g.transition = dissolve

#时长参数
init python:
    def get_audio_duration(channel="music"):
        duration = renpy.music.get_duration(channel)
        return convert_format(int(duration))
        
 
    def get_audio_position(channel="music"):
        music_pos = renpy.music.get_pos(channel)
        
        if music_pos:
            return convert_format(int(music_pos))
        return "00:00"
    #时间转换
    def convert_format(second):
        minute = second // 60
        second = second % 60
        result = ""

        #可用于59分59秒内音乐
        if minute:
            
            if minute < 10:
                result = '0' + str(minute) + ":" + str(second)
                if second < 10:
                    result ='0' + str(minute) + ":" '0' + str(second)
            else:
                result = str(minute) + ":" + str(second)
                if second < 10:
                    result = str(minute) + '0' + str(second)
                       
        else:

            if second < 10:
                result = '00:0' + str(second)
            else:
                result = '00:' + str(second)

        return result


#音乐列表顶部底部按钮定位
default extra_music_pos = ui.adjustment()

#鉴赏空间界面
screen extra(cg_page=0):
    tag menu
    add "gui/overlay/extra_menu.png" 
    #######画廊部分
    #CG列表
    viewport:
        xysize (1000, 600)
        xpos 40
        ypos 170
        vbox:
            #页数判断
            if (cg_page == 0):
                grid 3 3:
                    spacing 5
                    # if renpy.seen_image("bg03"):
                    #     add g.make_button("bg", "smbg03.png")
                    # else:
                    #     add g.make_button("unlock", "unknow.png")
                    #解锁判断，后续判断请自行添加

                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")  

                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")     

                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")      

            if (cg_page == 1):
                grid 3 3:
                    spacing 5
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")  

                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")     

                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")      
            if (cg_page == 2):
                grid 3 3:
                    spacing 5
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")  

                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")     

                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")
                    add g.make_button("bg", "images_s/test.png")      
    #翻页按钮
    hbox:
        xalign 0.3
        ypos 750
        spacing 40

        imagebutton:
            idle "gui/button/load_on_1.png"
            hover "gui/button/load_off_1.png"
            action Show("extra",cg_page=0)

        imagebutton:
            idle "gui/button/load_on_2.png"
            hover "gui/button/load_off_2.png"
            action Show("extra",cg_page=1)

        imagebutton:
            idle "gui/button/load_on_3.png"
            hover "gui/button/load_off_3.png"
            action Show("extra",cg_page=2)
    
    ######音乐部分
    #更新renpy.music.get_position()和get_music_duration()
    timer 0.1:
        action [SetVariable('duration',get_audio_duration()),SetVariable('music_pos',get_audio_position())]
        repeat True
    
    #音乐列表
    viewport id "MUSIC_list":
        mousewheel True #垂直滚动
        xysize (500, 550)
        xpos 1050
        ypos 120
        draggable True  #鼠标拖动可滚动视口
        yadjustment extra_music_pos #快速定位

        vbox:     
            spacing 10
            textbutton "桜吹雪の誓い\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/桜吹雪の誓い_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "Brand New Day\n-のる" action mr.Play("audio/BGM/Brand_New_Day_のる.ogg")
            textbutton "Close Love\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/Close_Love_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "Embers of a Vanishing Sky\n-MFP(Marron Fields Production)" action mr.Play("audio/BGM/Embers_of_a_Vanishing_Sky_MFP(Marron Fields Production).ogg")
            textbutton "Fighter's Edge\n-gooset" action mr.Play("audio/BGM/Fighter's_Edge_gooset.ogg")
            textbutton "Overcome\n-のる" action mr.Play("audio/BGM/Overcome_のる.ogg")
            textbutton "Umbra Protocol\n-松浦洋介" action mr.Play("audio/BGM/Umbra_Protocol_松浦洋介.ogg")
            textbutton "Under the Blue Fizz\n-松浦洋介" action mr.Play("audio/BGM/Under_the_Blue_Fizz_松浦洋介.ogg")
            textbutton "You Were the Last Light\n-松浦洋介" action mr.Play("audio/BGM/You_Were_the_Last_Light_松浦洋介.ogg")
            textbutton "Zen\n-yuhei komatsu" action mr.Play("audio/BGM/Zen_yuhei komatsu.ogg")
            textbutton "あくる日のワルツ\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/あくる日のワルツ_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "あたたかな雪\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/あたたかな雪_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "あの空に向かって\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/あの空に向かって_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "いつものカフェで待ち合わせ\n-秦暁" action mr.Play("audio/BGM/いつものカフェで待ち合わせ_秦暁.ogg")
            textbutton "かつての聖域\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/かつての聖域_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "ほのぼのいい天気\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/ほのぼのいい天気_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "タタリ\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/タタリ_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "別れの季節\n-alaki paca" action mr.Play("audio/BGM/別れの季節_alaki paca.ogg")
            textbutton "君影草\n-すもち" action mr.Play("audio/BGM/君影草_すもち.ogg")
            textbutton "夢の中を泳ぐ魚\n-ゆうきわたる" action mr.Play("audio/BGM/夢の中を泳ぐ魚_ゆうきわたる.ogg")
            textbutton "星空の導き\n-alaki paca" action mr.Play("audio/BGM/星空の導き_alaki paca.ogg")
            textbutton "晴れやかな日の午後に\n-しんさんわーくす" action mr.Play("audio/BGM/晴れやかな日の午後に_しんさんわーくす.ogg")
            textbutton "暗闇を駆け抜けろ！\n-alaki paca" action mr.Play("audio/BGM/暗闇を駆け抜けろ！_alaki paca.ogg")
            textbutton "桜が散る時\n-yuhei komatsu" action mr.Play("audio/BGM/桜が散る時_yuhei komatsu.ogg")
            textbutton "沈みゆく体、浮かぶ意識\n-alaki paca" action mr.Play("audio/BGM/沈みゆく体、浮かぶ意識_alaki paca.ogg")
            textbutton "祭りの夜\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/祭りの夜_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "言霊\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/言霊_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "路地裏ファンタジー\n-yuhei komatsu" action mr.Play("audio/BGM/路地裏ファンタジー_yuhei komatsu.ogg")
            textbutton "迫る闇\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/迫る闇_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "陰謀論\n-ゆうり(from Yuli Audio Craft)" action mr.Play("audio/BGM/陰謀論_ゆうり(from Yuli Audio Craft).ogg")
            textbutton "雪、吹き乱れて\n-蒲鉾さちこ" action mr.Play("audio/BGM/雪、吹き乱れて(Snow,blizzarding)_蒲鉾さちこ.ogg")
            # if mr.is_unlocked("bgm04.ogg"):
            #     textbutton "bgm04" action mr.Play("bgm04.ogg")
            # else:
            #     textbutton "???" action NullAction()

    
    # #功能按钮
    imagebutton:
        xpos 1510
        ypos 729
        idle "gui/overlay/config_pause_on.png"
        hover "gui/overlay/config_pause_off.png"
        selected_idle "gui/overlay/config_play_on.png"
        selected_hover "gui/overlay/config_play_off.png"
        if not renpy.music.is_playing() and not renpy.music.get_pause():
            action mr.Play(config.main_menu_music)
        else:
            action PauseAudio(channel="music",value="toggle")

    vbar:
        xysize (32, 600)
        xpos 1515 ypos 115
        bottom_bar "gui/slider/slider_vertical_off.png"
        top_bar "gui/slider/slider_vertical_on.png"
        thumb "gui/slider/thumb_vertical_on.png"
        value YScrollValue("MUSIC_list")

    bar:
        xpos 1050
        ypos 733
        xysize (440,32)
        right_bar "gui/slider/slider_horizontal_off.png"
        left_bar "gui/slider/slider_horizontal_on.png"
        thumb "gui/slider/thumb_horizontal_on.png"
        value AudioPositionValue(channel='music', update_interval=0.1)    

    #进度条，时长显示
    hbox:
        xpos 1050
        ypos 685
        xysize (440,32)
        python:
            duration = get_audio_duration()
            music_pos = get_audio_position()
        
        hbox:
            spacing 5
            xalign 0.5
            yalign 0.5
            text music_pos
            text "/"
            text duration
    
    key "mouseup_3" action [Stop('music'), Play("music", config.main_menu_music), Show("main_menu")]

    # 返回按钮
    imagebutton:
        align (0.95, 0.95)
        idle "gui/button/config_on_back.png"
        hover "gui/button/config_off_back.png"
        action [Stop('music'), Play("music", config.main_menu_music), Return()]


################################################################################
## 其他屏幕
################################################################################


## 确认屏幕 ########################################################################
##
## 当 Ren'Py 需要询问用户有关确定或取消的问题时，会调用确认屏幕。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    if  persistent.confirmation_dialog == False:
        on "show" action yes_action

    else:
        ## 显示此屏幕时，确保其他屏幕无法输入。
        modal True

        zorder 200

        #style_prefix "confirm"

        add "gui/overlay/confirm.png"

        text _(message):
            layout "subtitle"
            color "#dff2fc"
            size 32
            align (0.5,0.45)
            font "SourceHanSerifCN-SemiBold-7.otf"

        hbox:
            align (0.5,0.55)
            spacing 20
            imagebutton:
                idle "gui/button/confirm_on_yes.png"
                hover "gui/button/confirm_off_yes.png"
                action yes_action
            imagebutton:
                idle "gui/button/confirm_on_no.png"
                hover "gui/button/confirm_off_no.png"
                action no_action

        ## 右键点击退出并答复 no（取消）。
        key "game_menu" action no_action
        on "show" action MouseMove(730,495)


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## 快进指示屏幕 ######################################################################
##
## skip_indicator 屏幕用于指示快进正在进行中。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 8

            text _("正在快进")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## 此变换用于一个接一个地闪烁箭头。
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## 我们必须使用包含“▸”（黑色右旋小三角）字形的字体。
    font "DejaVuSans.ttf"


## 通知屏幕 ########################################################################
##
## 通知屏幕用于向用户显示消息。（例如，当游戏快速保存或进行截屏时。）
##
## https://doc.renpy.cn/zh-CN/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL 模式屏幕 ####################################################################
##
## 此屏幕用于 NVL 模式的对话和菜单。
##
## https://doc.renpy.cn/zh-CN/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## 在 vpgrid 或 vbox 中显示对话框。
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## 显示菜单，如果给定的话。如果 config.narrator_menu 设置为 True，则菜单
        ## 可能显示不正确。
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id



            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id

## 此语句控制一次可以显示的 NVL 模式条目的最大数量。
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## 对话气泡屏幕 ######################################################################
##
## 对话气泡屏幕用于以对话气泡的形式向玩家显示对话。对话气泡屏幕的参数与 say 屏幕
## 相同，必须创建一个 id 为 what 的可视控件，并且可以创建 id 为 namebox、who 和
## window 的可视控件。
##
## https://doc.renpy.cn/zh-CN/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## 移动设备界面
################################################################################

# style pref_vbox:
#     variant "medium"
#     xsize 563

# ## 由于可能没有鼠标，我们将快捷菜单替换为一个使用更少、更大按钮的版本，这样更容
# ## 易触摸。
# screen quick_menu():
#     variant "touch"

#     zorder 100

#     if quick_menu:

#         hbox:
#             style_prefix "quick"

#             xalign 0.5
#             yalign 1.0

#             textbutton _("回退") action Rollback()
#             textbutton _("快进") action Skip() alternate Skip(fast=True, confirm=persistent.confirmation_dialog)
#             textbutton _("自动") action Preference("auto-forward", "toggle")
#             textbutton _("菜单") action ShowMenu()


# style window:
#     variant "small"
#     background "gui/phone/textbox.png"

# style radio_button:
#     variant "small"
#     foreground "gui/phone/button/radio_[prefix_]foreground.png"

# style check_button:
#     variant "small"
#     foreground "gui/phone/button/check_[prefix_]foreground.png"

# style nvl_window:
#     variant "small"
#     background "gui/phone/nvl.png"

# style main_menu_frame:
#     variant "small"
#     background "gui/phone/overlay/main_menu.png"

# style game_menu_outer_frame:
#     variant "small"
#     background "gui/phone/overlay/game_menu.png"

# style game_menu_navigation_frame:
#     variant "small"
#     xsize 425

# style game_menu_content_frame:
#     variant "small"
#     top_margin 0

# style pref_vbox:
#     variant "small"
#     xsize 500

# style bar:
#     variant "small"
#     ysize gui.bar_size
#     left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
#     right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

# style vbar:
#     variant "small"
#     xsize gui.bar_size
#     top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
#     bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

# style scrollbar:
#     variant "small"
#     ysize gui.scrollbar_size
#     base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
#     thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

# style vscrollbar:
#     variant "small"
#     xsize gui.scrollbar_size
#     base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
#     thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

# style slider:
#     variant "small"
#     ysize gui.slider_size
#     base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
#     thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

# style vslider:
#     variant "small"
#     xsize gui.slider_size
#     base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
#     thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

# style slider_vbox:
#     variant "small"
#     xsize None

# style slider_slider:
#     variant "small"
#     xsize 750
