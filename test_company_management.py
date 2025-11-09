"""
会社管理システムのpytestテストコード

元のコードをテストするためのpytestテストスイートです。
"""

import pytest
from unittest.mock import patch
from company_management import (
    Gender, Post, Human, Employee, President, Company
)


class TestGenderEnum:
    """Gender列挙型のテスト"""

    def test_gender_values(self):
        """性別の値が正しいことを確認"""
        assert Gender.MAN.value == "男性"
        assert Gender.WOMAN.value == "女性"
        assert Gender.OTHER.value == "その他"


class TestPostEnum:
    """Post列挙型のテスト"""

    def test_post_values(self):
        """役職の値が正しいことを確認"""
        assert Post.HIRA.value == "ヒラ"
        assert Post.SYUNIN.value == "主任"
        assert Post.KATYO.value == "課長"
        assert Post.YARUIN.value == "役員"


class TestHuman:
    """Humanクラスのテスト"""

    def test_human_initialization(self):
        """Humanの初期化テスト"""
        human = Human("山田太郎", Gender.MAN, 30)
        assert human.name == "山田太郎"
        assert human.gender == Gender.MAN
        assert human.age == 30

    def test_human_self_introduction(self, capsys):
        """自己紹介のテスト"""
        human = Human("山田花子", Gender.WOMAN, 25)
        human.do_self_introduction()
        captured = capsys.readouterr()
        assert "山田花子" in captured.out
        assert "女性" in captured.out
        assert "25歳" in captured.out


class TestEmployee:
    """Employeeクラスのテスト"""

    def test_employee_initialization(self):
        """社員の初期化テスト"""
        employee = Employee("佐藤太郎", Gender.MAN, 22, Post.HIRA)
        assert employee.name == "佐藤太郎"
        assert employee.gender == Gender.MAN
        assert employee.age == 22
        assert employee.post == Post.HIRA
        assert len(employee.id) == 4
        assert employee.id.isdigit()

    def test_employee_salary(self):
        """給与のテスト"""
        hira = Employee("A", Gender.MAN, 25, Post.HIRA)
        syunin = Employee("B", Gender.MAN, 30, Post.SYUNIN)
        katyo = Employee("C", Gender.MAN, 35, Post.KATYO)
        yaruin = Employee("D", Gender.MAN, 40, Post.YARUIN)

        assert hira.salary == 200000
        assert syunin.salary == 300000
        assert katyo.salary == 450000
        assert yaruin.salary == 600000

    def test_employee_self_introduction(self, capsys):
        """社員の自己紹介テスト"""
        employee = Employee("田中三郎", Gender.MAN, 33, Post.SYUNIN)
        employee.do_self_introduction()
        captured = capsys.readouterr()
        assert "田中三郎" in captured.out
        assert "男性" in captured.out
        assert "33歳" in captured.out
        assert "主任" in captured.out

    def test_employee_promote(self, capsys):
        """昇進テスト"""
        employee = Employee("昇進太郎", Gender.MAN, 30, Post.HIRA)
        
        employee.promote()
        assert employee.post == Post.SYUNIN
        
        employee.promote()
        assert employee.post == Post.KATYO
        
        employee.promote()
        assert employee.post == Post.YARUIN
        
        # 最高役職での昇進試行
        employee.promote()
        assert employee.post == Post.YARUIN
        captured = capsys.readouterr()
        assert "すでに最高役職" in captured.out

    def test_employee_demote(self, capsys):
        """降格テスト"""
        employee = Employee("降格太郎", Gender.MAN, 40, Post.YARUIN)
        
        employee.demote()
        assert employee.post == Post.KATYO
        
        employee.demote()
        assert employee.post == Post.SYUNIN
        
        employee.demote()
        assert employee.post == Post.HIRA
        
        # 最低役職での降格試行
        employee.demote()
        assert employee.post == Post.HIRA
        captured = capsys.readouterr()
        assert "すでに最低役職" in captured.out


class TestPresident:
    """Presidentクラスのテスト"""

    def test_president_initialization(self):
        """社長の初期化テスト"""
        president = President("倍井杉蔵", Gender.MAN, 88)
        assert president.name == "倍井杉蔵"
        assert president.gender == Gender.MAN
        assert president.age == 88
        assert president.salary == 1000000
        assert president.company is None

    def test_president_self_introduction(self, capsys):
        """社長の自己紹介テスト"""
        president = President("社長太郎", Gender.MAN, 60)
        president.do_self_introduction()
        captured = capsys.readouterr()
        assert "社長太郎" in captured.out
        assert "男性" in captured.out
        assert "60歳" in captured.out
        assert "社長" in captured.out

    def test_president_company_setter(self):
        """会社設定のテスト"""
        president = President("社長太郎", Gender.MAN, 60)
        company = Company()
        president.company = company
        assert president.company == company

    def test_president_get_personnel_by_name(self):
        """名前で社員検索テスト"""
        president = President("社長太郎", Gender.MAN, 60)
        company = Company()
        president.company = company
        
        company.add_employee("佐藤太郎", Gender.MAN, 30, Post.HIRA)
        
        found = president.get_personnel_by_name("佐藤太郎")
        assert found is not None
        assert found.name == "佐藤太郎"
        
        not_found = president.get_personnel_by_name("存在しない人")
        assert not_found is None

    def test_president_get_personnel_by_id(self):
        """IDで社員検索テスト"""
        president = President("社長太郎", Gender.MAN, 60)
        company = Company()
        president.company = company
        
        company.add_employee("鈴木次郎", Gender.MAN, 25, Post.HIRA)
        employee = company.employees[0]
        
        found = president.get_personnel_by_id(employee.id)
        assert found is not None
        assert found.id == employee.id

    def test_president_add_employee(self, capsys):
        """社長による社員追加テスト"""
        president = President("社長太郎", Gender.MAN, 60)
        company = Company()
        president.company = company
        
        president.add_employee("新入社員", Gender.MAN, 22, Post.HIRA)
        assert company.current_number == 1

    def test_president_delete_employee(self, capsys):
        """社長による社員削除テスト"""
        president = President("社長太郎", Gender.MAN, 60)
        company = Company()
        president.company = company
        
        company.add_employee("削除対象", Gender.MAN, 30, Post.HIRA)
        employee = company.employees[0]
        
        president.delete_employee(employee)
        assert company.current_number == 0

    def test_president_resignation_with_employees(self, capsys):
        """社員がいる場合の辞任テスト"""
        president = President("旧社長", Gender.MAN, 70)
        company = Company()
        president.company = company
        
        company.add_employee("次期社長", Gender.MAN, 50, Post.YARUIN)
        
        new_president = president.resignation()
        
        assert new_president is not None
        assert new_president.name == "次期社長"
        assert new_president.company == company
        assert company.current_number == 0  # 次期社長は社員リストから削除される

    def test_president_resignation_without_employees(self, capsys):
        """社員がいない場合の辞任テスト"""
        president = President("孤独な社長", Gender.MAN, 70)
        company = Company()
        president.company = company
        
        new_president = president.resignation()
        
        assert new_president is None
        captured = capsys.readouterr()
        assert "辞任しないでください" in captured.out


class TestCompany:
    """Companyクラスのテスト"""

    def test_company_initialization(self):
        """会社の初期化テスト"""
        company = Company()
        assert company.current_number == 0
        assert len(company.employees) == 0
        assert company.MAX_NUMBER_OF_PEOPLE == 10

    def test_company_add_employee(self, capsys):
        """社員追加テスト"""
        company = Company()
        company.add_employee("新入社員", Gender.MAN, 22, Post.HIRA)
        
        assert company.current_number == 1
        assert company.employees[0].name == "新入社員"

    def test_company_add_employee_max_limit(self, capsys):
        """社員数上限テスト"""
        company = Company()
        
        # 上限まで追加
        for i in range(Company.MAX_NUMBER_OF_PEOPLE):
            company.add_employee(f"社員{i}", Gender.MAN, 25, Post.HIRA)
        
        assert company.current_number == Company.MAX_NUMBER_OF_PEOPLE
        
        # 上限を超えて追加しようとする
        company.add_employee("超過社員", Gender.MAN, 30, Post.HIRA)
        assert company.current_number == Company.MAX_NUMBER_OF_PEOPLE
        captured = capsys.readouterr()
        assert "上限" in captured.out

    def test_company_delete_employee(self, capsys):
        """社員削除テスト"""
        company = Company()
        company.add_employee("削除対象", Gender.MAN, 30, Post.HIRA)
        employee = company.employees[0]
        
        company.delete_employee(employee)
        assert company.current_number == 0

    def test_company_delete_nonexistent_employee(self, capsys):
        """存在しない社員の削除テスト"""
        company = Company()
        fake_employee = Employee("存在しない", Gender.MAN, 30, Post.HIRA)
        
        company.delete_employee(fake_employee)
        captured = capsys.readouterr()
        assert "存在しません" in captured.out

    def test_company_get_personnel_by_name(self):
        """名前で社員検索テスト"""
        company = Company()
        company.add_employee("検索対象", Gender.WOMAN, 28, Post.SYUNIN)
        
        found = company.get_personnel_by_name("検索対象")
        assert found is not None
        assert found.name == "検索対象"
        
        not_found = company.get_personnel_by_name("存在しない")
        assert not_found is None

    def test_company_get_personnel_by_id(self):
        """IDで社員検索テスト"""
        company = Company()
        company.add_employee("ID検索", Gender.MAN, 30, Post.HIRA)
        employee = company.employees[0]
        
        found = company.get_personnel_by_id(employee.id)
        assert found is not None
        assert found.id == employee.id

    def test_company_select_president_with_executive(self):
        """役員がいる場合の次期社長選出テスト"""
        company = Company()
        company.add_employee("若手役員", Gender.MAN, 45, Post.YARUIN)
        company.add_employee("ベテラン役員", Gender.MAN, 55, Post.YARUIN)
        company.add_employee("平社員", Gender.MAN, 60, Post.HIRA)
        
        next_president = company.select_president()
        
        assert next_president is not None
        assert next_president.post == Post.YARUIN
        assert next_president.age == 55  # 役員の中で最年長

    def test_company_select_president_without_executive(self):
        """役員がいない場合の次期社長選出テスト"""
        company = Company()
        company.add_employee("若手", Gender.MAN, 25, Post.HIRA)
        company.add_employee("中堅", Gender.MAN, 35, Post.SYUNIN)
        company.add_employee("ベテラン", Gender.MAN, 50, Post.KATYO)
        
        next_president = company.select_president()
        
        assert next_president is not None
        assert next_president.age == 50  # 全社員の中で最年長

    def test_company_select_president_empty(self):
        """社員がいない場合の次期社長選出テスト"""
        company = Company()
        
        next_president = company.select_president()
        assert next_president is None

    def test_company_display_all_employees(self, capsys):
        """社員一覧表示テスト"""
        company = Company()
        company.add_employee("表示太郎", Gender.MAN, 30, Post.HIRA)
        company.add_employee("表示花子", Gender.WOMAN, 28, Post.SYUNIN)
        
        company.display_all_employees()
        captured = capsys.readouterr()
        
        assert "社員一覧" in captured.out
        assert "表示太郎" in captured.out
        assert "表示花子" in captured.out
        assert "合計: 2名" in captured.out

    def test_company_display_empty_employees(self, capsys):
        """社員がいない場合の一覧表示テスト"""
        company = Company()
        
        company.display_all_employees()
        captured = capsys.readouterr()
        
        assert "社員がいません" in captured.out


class TestIntegration:
    """統合テスト"""

    def test_complete_workflow(self, capsys):
        """完全なワークフローのテスト"""
        # 会社と社長の作成
        president = President("統合テスト社長", Gender.MAN, 65)
        company = Company()
        president.company = company
        
        # 複数の社員を追加
        president.add_employee("社員A", Gender.MAN, 30, Post.HIRA)
        president.add_employee("社員B", Gender.WOMAN, 35, Post.SYUNIN)
        president.add_employee("社員C", Gender.MAN, 45, Post.YARUIN)
        
        assert company.current_number == 3
        
        # 検索と昇進
        employee = president.get_personnel_by_name("社員A")
        assert employee is not None
        employee.promote()
        assert employee.post == Post.SYUNIN
        
        # 辞任と新社長就任
        new_president = president.resignation()
        assert new_president is not None
        assert new_president.name == "社員C"
        assert company.current_number == 2  # 新社長は社員リストから削除

    def test_edge_cases(self):
        """エッジケースのテスト"""
        company = Company()
        
        # 空の会社での検索
        assert company.get_personnel_by_name("誰もいない") is None
        assert company.get_personnel_by_id("0000") is None
        
        # 次期社長選出（社員なし）
        assert company.select_president() is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
