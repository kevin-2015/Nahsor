import allure
import pytest
import win_unicode_console
win_unicode_console.enable()



@allure.title("测试报告")
@allure.feature('testsuite1')
@allure.story('testcass1')
def test_minor():
    assert 1


@allure.feature('testsuite2')
@allure.story('testcass2', 'testcass3', 'testcass4')
class TestBar:
    # will have 'Feature2 and Story2 and Story3 and Story4'
    @allure.title("测试报告1")
    def test_bar1(self):
        with allure.step("步骤一"):
            assert True
        with allure.step("步骤二"):
            assert True
        with allure.step("步骤三"):
            assert True
    @allure.title("测试报告2")
    def test_bar2(self):
        with allure.step("步骤一"):
            assert True
        with allure.step("步骤二"):
            assert True
        with allure.step("步骤三"):
            allure.attach('失败的步骤', '具体内容')
            assert False
    @allure.title("测试报告3")
    def test_bar3(self):
        with allure.step("步骤一"):
            assert True
        with allure.step("步骤二"):
            assert True
        with allure.step("步骤三"):
            assert True
        login()


@allure.step('外部调用的步骤')
def login():
    assert True