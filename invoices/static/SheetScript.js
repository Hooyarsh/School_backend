//19 Esfand

function doPost(e) {
    Logger.log(e);  // ثبت محتوای e برای دیباگ

    // بررسی وجود پارامترها
    if (!e || !e.parameters) {
        return ContentService.createTextOutput(JSON.stringify({ result: "error", message: "No parameters provided." }))
            .setMimeType(ContentService.MimeType.JSON);
    }

    // دسترسی به شیت
    const sheet = SpreadsheetApp.openById('1VgG0fniu7m2EwuM7ryLps1OEoSsZrkH_jO37ojdadCQ').getActiveSheet();

    // استخراج پارامترهای فاکتور
    const timestamp = e.parameter.submitTimestamp || "";
    const invoiceNumber = e.parameter.invoiceNumber || "";
    const invoiceDate = e.parameter.invoiceDate || "";
    const totalAmount = e.parameter.totalAmount || "";
    const finalSupplierDetails = e.parameter.finalSupplierDetails || "";
    const finalDescription = e.parameter.finalDescription || "";

    // آماده‌سازی اطلاعات آیتم‌ها
    const items = [];
    let i = 1;
    while (e.parameters['itemCount' + i]) {
        const itemCount = e.parameters['itemCount' + i] || "";
        const level = e.parameters['level' + i] || "";
        const invoiceType = e.parameters['invoiceType' + i] || "";
        const nationalID = e.parameters['nationalID' + i] || "";
        const subGroup = e.parameters['subGroup' + i] || "";
        const itemCategory = e.parameters['itemCategory' + i] || "";
        const subCode = e.parameters['subCode' + i] || "";
        const detailCode = e.parameters['detailCode' + i] || "";
        const otherDetail = e.parameters['otherDetailCode' + i] || "";
        const unitPrice = e.parameters['unitPrice' + i] || "";

        // افزودن موارد به آرایه items
        items.push([
            itemCount.toString(),
            unitPrice.toString(),
            level.toString(),
            invoiceType.toString(),
            subGroup.toString(),
            nationalID.toString(),
            itemCategory.toString(),
            subCode.toString(),
            detailCode.toString(),
            otherDetail.toString()
        ]);
        i++;
    }

    // ثبت اطلاعات در شیت
    let itemIndex = 1;

    items.forEach(item => {
        const itemRow = [
            timestamp.toString(),
            invoiceNumber.toString(),
            invoiceDate.toString(),
            totalAmount.toString(),
            itemIndex,
            ...item,
            finalSupplierDetails.toString(),
            finalDescription.toString(),
            0 // مقدار پیش‌فرض برای تعدادی که بعداً محاسبه می‌شود
        ];
        sheet.appendRow(itemRow);
        itemIndex++;
    });

    // پردازش داده‌های جدید
    const stdSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('STD');
    const stdData = stdSheet.getDataRange().getValues();
    const tanKhahSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('TanKhah');
    const tanKhahData = tanKhahSheet.getDataRange().getValues();

    try {
        let inIndex = 1;

        // پردازش هر قلم کالا
        items.forEach((item, itemIndex) => {
            const id = formatID(item[5]);
            const grade = item[2];
            const kind = item[3];
            const subgroup = item[4];
            const indate = invoiceDate;

            Logger.log(`Processing item: Kind=${kind}, ID=${id}, InDate=${indate}, Grade=${grade}, Subgroup=${subgroup}`);

            // شمارش افراد مناسب برای هر قلم
            let countForThisItem = 0;
            const relatedStudents = []; // مرتبط با همین قلم

            // پردازش بر اساس نوع فاکتور
            if (kind === 'فردی') {
                for (let j = 0; j < stdData.length; j++) {
                    const idStd = stdData[j][0];
                    const rdate = stdData[j][5];
                    const ddate = stdData[j][6];
                    const gradeStd = stdData[j][2];

                    if (grade === gradeStd && id === idStd && indate <= ddate && indate >= rdate) {
                        countForThisItem++;
                        relatedStudents.push(idStd);

                        let columnToUpdate = 9;
                        while (stdSheet.getRange(j + 1, columnToUpdate).getValue() !== "") {
                            columnToUpdate++;
                        }
                        stdSheet.getRange(j + 1, columnToUpdate).setValue(invoiceNumber + '-' + inIndex);
                    }
                }
            } else if (kind === 'زیرگروه زبان') {
                for (let j = 0; j < stdData.length; j++) {
                    const subgroupStd = stdData[j][4];
                    const ddate = stdData[j][6];
                    const rdate = stdData[j][5];
                    const gradeStd = stdData[j][2];

                    if (grade === gradeStd && subgroup === subgroupStd && indate <= ddate && indate >= rdate) {
                        countForThisItem++;
                        relatedStudents.push(stdData[j][0]);

                        let columnToUpdate = 9;
                        while (stdSheet.getRange(j + 1, columnToUpdate).getValue() !== "") {
                            columnToUpdate++;
                        }
                        stdSheet.getRange(j + 1, columnToUpdate).setValue(invoiceNumber + '-' + inIndex);
                    }
                }
            } else {
                for (let j = 0; j < stdData.length; j++) {
                    const ddate = stdData[j][6];
                    const rdate = stdData[j][5];
                    const gradeStd = stdData[j][2];

                    if (grade === gradeStd && indate <= ddate && indate >= rdate) {
                        countForThisItem++;
                        relatedStudents.push(stdData[j][0]);

                        let columnToUpdate = 9;
                        while (stdSheet.getRange(j + 1, columnToUpdate).getValue() !== "") {
                            columnToUpdate++;
                        }
                        stdSheet.getRange(j + 1, columnToUpdate).setValue(invoiceNumber + '-' + inIndex);
                    }
                }
            }

            // ثبت تعداد و محاسبه pricePerPerson
            const rowIndex = sheet.getLastRow() - items.length + itemIndex + 1; 
            sheet.getRange(rowIndex, 18).setValue(countForThisItem); 
            
            const itemCount = parseFloat(item[0]); 
            const unitPrice = parseFloat(item[1]); 
            const pricePerPerson = countForThisItem > 0 ? itemCount * unitPrice / countForThisItem : 0; 
            sheet.getRange(rowIndex, 19).setValue(pricePerPerson); 

            // ثبت pricePerPerson در شیت TanKhah برای دانش‌آموزان مرتبط با همین قلم
            relatedStudents.forEach(studentId => {
                for (let k = 0; k < tanKhahData.length; k++) {
                    if (tanKhahData[k][0] === studentId) { 
                      let columnToUpdate = 9;
                      while (tanKhahSheet.getRange(k + 1, columnToUpdate).getValue() !== "") {
                            columnToUpdate++;
                      }
                      // اطمینان از تبدیل مقدار ستون هشتم به عدد
                      const currentTanKhahValue = parseFloat(tanKhahSheet.getRange(k + 1, 8).getValue()) || 0;
                      const newTanKhahValue = currentTanKhahValue + pricePerPerson; // به‌روزرسانی مقدار تنخواه
                      tanKhahSheet.getRange(k + 1, 8).setValue(newTanKhahValue); // ثبت مقدار جدید در شیت TanKhah
                      tanKhahSheet.getRange(k + 1, columnToUpdate).setValue(pricePerPerson); // ثبت pricePerPerson جدید

                      // به‌روزرسانی شیت STD
                      const stdRowIndex = k + 1; // همان ردیف در شیت STD
                      stdSheet.getRange(stdRowIndex, 8).setValue(newTanKhahValue); // ثبت مقدار جدید در شیت STD

                      break; 
                  }
              }
          });

            inIndex++;
        });
    } catch (error) {
        Logger.log(`Error processing new submission: ${error}`);
    }

    return ContentService.createTextOutput(JSON.stringify({ result: "success" }))
        .setMimeType(ContentService.MimeType.JSON);
}

// تابعی برای فرمت کردن کد ملی و حفظ صفرهای ابتدایی
function formatID(id) {
    if (id === "") {
        return "";
    }
    return id.toString().padStart(10, '0');
}
