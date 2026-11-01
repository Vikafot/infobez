from pathlib import Path
from xml.sax.saxutils import escape as экранировать
from zipfile import ZipFile as Архив, ZIP_DEFLATED as СЖАТИЕ
from datetime import datetime as ДатаВремя, timezone as Пояс, timedelta as Интервал

def дата_сейчас():
    return ДатаВремя.now(Пояс(Интервал(hours=7))).strftime('%d.%m.%Y')

def сохранить_документ(путь, заголовок, абзацы):
    """Минимальный DOCX в стандартном OOXML, только стандартная библиотека."""
    тело=[]
    for номер,текст in enumerate([заголовок]+абзацы):
        свойства='<w:pPr><w:jc w:val="center"/></w:pPr>' if номер==0 else ''
        тело.append('<w:p>'+свойства+'<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="28"/>'+
                    ('<w:b/>' if номер==0 else '')+'</w:rPr><w:t xml:space="preserve">'+экранировать(str(текст))+'</w:t></w:r></w:p>')
    текст='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+''.join(тело)+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701"/></w:sectPr></w:body></w:document>'
    with Архив(путь,'w',СЖАТИЕ) as архив:
        архив.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        архив.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
        архив.writestr('word/document.xml',текст)

def текст_акта(организация,система,расчёт,дата):
    return [организация['название'], 'УЧЕБНЫЙ ОБРАЗЕЦ. Все сведения об организации вымышленные.',
      'УТВЕРЖДАЮ: руководитель проекта '+организация['руководитель_проекта']+' __________',
      f'Акт №{система["номер"]} от {дата}. Город: {организация["город"]}.',
      'Комиссия: председатель — '+организация['руководитель_проекта']+'; ответственный за ПДн — '+организация['ответственный_за_защиту_пдн']+'.',
      'Система: '+система['номер']+' — '+система['название'], 'Границы: '+система['границы_системы'],
      'Категория: '+система['категория_пдн']+'; примеры: '+', '.join(система['примеры_данных']),
      f'Группа субъектов: {система["тип_субъектов"]}; количество: {система["количество_субъектов"]}; заданный тип угроз: {система["тип_угроз_по_условию"]}.',
      'Признак ГИС: '+система['является_гис']+'. Тип угроз принят по условию, не выведен из ПО.',
      'Основание: ПП РФ от 01.11.2012 №1119, пп.9–12; учебная матрица данные/матрица_уз.py.',
      'Решение комиссии (учебный расчёт): '+расчёт['уровень'],расчёт['обоснование'],
      'Прежний заявленный уровень: '+str(система.get('заявленный_уз')),
      'Расхождение: '+('обнаружено; требуется переутверждение' if система.get('заявленный_уз') and система['заявленный_уз']!=расчёт['уровень'] else 'нет'),
      'Меры защиты: по расширенному учебному профилю приказа №21; см. план мер и ТЗ.',
      'Пересмотр: при изменении границ, состава данных, числа субъектов или модели угроз.',
      'Подписи комиссии: ____________________ / ____________________',
      'Структура сверена с опубликованным образцом: https://gramotaib.ru/obraztsy/akt-opredeleniya-urovnya-zashchishchennosti-pdn ; текст составлен самостоятельно.']
