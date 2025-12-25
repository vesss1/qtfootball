#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    
    // Connect the add button to the slot
    connect(ui->pushButtonAdd, &QPushButton::clicked, this, &MainWindow::onAddPlayerClicked);
    
    // Set table properties
    ui->tableWidgetPlayers->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->tableWidgetPlayers->horizontalHeader()->setStretchLastSection(true);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::onAddPlayerClicked()
{
    QString name = ui->lineEditName->text().trimmed();
    QString position = ui->comboBoxPosition->currentText();
    int age = ui->spinBoxAge->value();
    
    // Validate name
    if (name.isEmpty()) {
        QMessageBox::warning(this, "警告", "請輸入球員姓名！");
        return;
    }
    
    // Create player and add to list
    Player player;
    player.name = name;
    player.position = position;
    player.age = age;
    players.append(player);
    
    // Add to table
    int row = ui->tableWidgetPlayers->rowCount();
    ui->tableWidgetPlayers->insertRow(row);
    ui->tableWidgetPlayers->setItem(row, 0, new QTableWidgetItem(name));
    ui->tableWidgetPlayers->setItem(row, 1, new QTableWidgetItem(position));
    ui->tableWidgetPlayers->setItem(row, 2, new QTableWidgetItem(QString::number(age)));
    
    // Clear input fields
    ui->lineEditName->clear();
    ui->comboBoxPosition->setCurrentIndex(0);
    ui->spinBoxAge->setValue(20);
    
    // Show success message
    QMessageBox::information(this, "成功", QString("球員 %1 已新增！").arg(player.name));
}
