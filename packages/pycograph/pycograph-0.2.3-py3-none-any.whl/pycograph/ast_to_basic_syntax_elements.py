"""Parse the abstract syntax tree of a Python project into basic syntax element objects."""
import ast
from typing import List, Union

from pycograph.schemas.basic_syntax_elements import (
    CallSyntaxElement,
    ClassDefSyntaxElement,
    ConstantSyntaxElement,
    FunctionDefSyntaxElement,
    ImportSyntaxElement,
    SyntaxElement,
    ImportFromSyntaxElement,
)


def parse_module(content: str, full_name: str) -> List[SyntaxElement]:
    result = []
    module = ast.parse(content, full_name, type_comments=True)
    for ast_object in module.body:
        result.extend(parse_ast_object(ast_object))
    return result


def parse_ast_object(ast_object: ast.AST) -> List[SyntaxElement]:
    if type(ast_object) == ast.ImportFrom:
        return parse_import_from(ast_object)  # type: ignore
    if type(ast_object) == ast.Import:
        return parse_import(ast_object)  # type: ignore
    if type(ast_object) == ast.FunctionDef:
        return [parse_function(ast_object)]  # type: ignore
    if type(ast_object) == ast.ClassDef:
        return [parse_class(ast_object)]  # type: ignore

    if type(ast_object) == ast.Assign:
        return parse_ast_assign(ast_object)  # type: ignore

    if type(ast_object) == ast.Attribute:
        result = parse_ast_attribute(ast_object)  # type: ignore
        if result:
            return [result]
    if type(ast_object) == ast.Name:
        result = parse_ast_name(ast_object)  # type: ignore
        if result:
            return [result]
    return []


def parse_import_from(ast_import_from: ast.ImportFrom):
    result = []
    for import_from_name in ast_import_from.names:
        import_relationship = ImportFromSyntaxElement(
            from_text=ast_import_from.module,
            name=import_from_name.name,
            as_name=import_from_name.asname,
            level=ast_import_from.level,
        )
        result.append(import_relationship)
    return result


def parse_import(ast_import: ast.Import):
    result = []
    for import_from_name in ast_import.names:
        import_relationship = ImportSyntaxElement(
            name=import_from_name.name,
            as_name=import_from_name.asname,
        )
        result.append(import_relationship)
    return result


def parse_function(ast_function_def: ast.FunctionDef) -> FunctionDefSyntaxElement:
    function_def = FunctionDefSyntaxElement(name=ast_function_def.name)
    for line in ast.walk(ast_function_def):
        if type(line) != ast.FunctionDef:
            function_def.add_syntax_elements(parse_ast_object(line))
    return function_def


def parse_class(ast_class: ast.ClassDef) -> ClassDefSyntaxElement:
    class_def = ClassDefSyntaxElement(name=ast_class.name)

    # Here, we don't use walk,
    # because we want to add only the direct children.
    # We assume that we won't encounter ifs or other similar blocks
    # directly in the class's code, but rather in functions...
    for ast_object in ast_class.body:
        class_def.add_syntax_elements(parse_ast_object(ast_object))

    return class_def


def parse_ast_assign(ast_assign: ast.Assign) -> List[SyntaxElement]:
    result = []
    for target in ast_assign.targets:
        if type(target) == ast.Name:
            parsed_name = parse_ast_name(target)  # type: ignore
            if parsed_name:
                result.append(parsed_name)
    return result


def parse_ast_attribute(ast_attribute: ast.Attribute) -> Union[SyntaxElement, None]:
    if type(ast_attribute.value) == ast.Name:
        return parse_ast_name(ast_attribute.value, ast_attribute.attr)  # type: ignore
    if (
        type(ast_attribute.value) == ast.Call
        and type(ast_attribute.value.func) == ast.Name  # type: ignore
    ):
        return parse_ast_name(ast_attribute.value.func, ast_attribute.attr)  # type: ignore
    return None


def parse_ast_name(
    ast_name: ast.Name, called_attribute: str = None
) -> Union[SyntaxElement, None]:
    if type(ast_name.ctx) == ast.Load:
        return parse_loaded_ast_name(ast_name, called_attribute)
    if type(ast_name.ctx) == ast.Store:
        if ast_name.id == ast_name.id.upper():
            return parse_constant_definition(ast_name)
    return None


def parse_constant_definition(ast_name: ast.Name) -> ConstantSyntaxElement:
    return ConstantSyntaxElement(name=ast_name.id)


def parse_loaded_ast_name(
    ast_name: ast.Name, called_attribute: str = None
) -> CallSyntaxElement:
    return CallSyntaxElement(
        what_reference_name=ast_name.id,
        called_attribute=called_attribute,
    )
