def menu():
    print('功能列表-------------')
    print('1. 添加学员')
    print('2. 删除学员')
    print('3. 修改学员')
    print('4. 查询学员')
    print('5. 显示学员')
    print('6. 退出系统')
    print('--------------------')


def add_member():
    global members
    m_id, m_name, m_phone = input('请输入学号:'), input('请输入姓名:'), input('请输入手机号:')
    for member in members:
        if member['name'] == m_name:
            print('用户已存在\n')
            return
    members.append({'id': m_id, 'name': m_name, 'phone': m_phone})
    print('添加成功\n')


def del_member():
    global members
    name = input('请输入要删除的学员姓名:')
    for member in members:
        if member['name'] == name:
            print(f"学号:{member['id']}\t姓名:{member['name']}\t手机号:{member['phone']}")
            cmd = input('确定删除此学员？Y/N')
            if cmd == 'Y':
                members.remove(member)
                print('删除成功\n')
                break
            else:
                print('取消删除\n')
                break
    else:
        print('该学员不存在\n')


def edit_member():
    global members
    name = input('请输入要修改的学员姓名:')
    for member in members:
        if member['name'] == name:
            print(f"学号:{member['id']}\t姓名:{member['name']}\t手机号:{member['phone']}")
            try:
                cmd = int(input('请输入需要修改的学员项目:\n1:学号\t2:姓名\t3：手机号'))
            except ValueError:
                print('输入错误\n')
                return
            if cmd == 1:
                member['id'] = input('请输入学员学号:')
                print('修改成功\n')
                return
            elif cmd == 2:
                name = input('请输入学员姓名:')
                for m in members:
                    if m['name'] == name:
                        print('该学员已存在\n')
                        return
                else:
                    member['name'] = name
                    print('修改成功\n')
                    return
            elif cmd == 3:
                member['phone'] = input('请输入学员手机号')
                print('修改成功\n')
                return
            else:
                print('输入错误\n')
                return
    else:
        print('该学员不存在\n')


def search_member():
    global members
    name = input('请输入要查找的学员姓名:')
    for member in members:
        if member['name'] == name:
            print(f"学号:{member['id']}\t姓名:{member['name']}\t手机号:{member['phone']}\n")
            return
    else:
        print('该学员不存在\n')


def show_members():
    global members
    for member in members:
        print(f"学号:{member['id']}\t姓名:{member['name']}\t手机号:{member['phone']}")
    print()


def do(cmd):
    if cmd == 1:
        add_member()
    elif cmd == 2:
        del_member()
    elif cmd == 3:
        edit_member()
    elif cmd == 4:
        search_member()
    elif cmd == 5:
        show_members()
    else:
        print('输入错误\n')


def run():
    while True:
        # 显示界面
        menu()
        try:
            cmd = int(input('请选择功能:'))
        except ValueError:
            print('输入错误\n')
            continue
        # 执行功能
        if cmd != 6:
            do(cmd)
        elif input('确认退出？ Y/N') == 'Y':
            break
    print('退出系统')


if __name__ == '__main__':
    members = []
    run()
