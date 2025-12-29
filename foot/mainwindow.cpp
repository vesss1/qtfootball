#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , currentAttempts(0)
    , currentSuccessfulGoals(0)
    , currentDistance(8)
    , practiceInProgress(false)
{
    ui->setupUi(this);
    
    // Connect the add button to the slot
    connect(ui->pushButtonAdd, &QPushButton::clicked, this, &MainWindow::onAddPlayerClicked);
    
    // Connect practice tracking buttons
    connect(ui->pushButtonStartPractice, &QPushButton::clicked, this, &MainWindow::onStartPracticeClicked);
    connect(ui->pushButtonRecordGoal, &QPushButton::clicked, this, &MainWindow::onRecordGoalClicked);
    connect(ui->pushButtonRecordMiss, &QPushButton::clicked, this, &MainWindow::onRecordMissClicked);
    connect(ui->pushButtonEndPractice, &QPushButton::clicked, this, &MainWindow::onEndPracticeClicked);
    connect(ui->pushButtonShowStats, &QPushButton::clicked, this, &MainWindow::onShowStatsClicked);
    
    // Set table properties
    ui->tableWidgetPlayers->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->tableWidgetPlayers->horizontalHeader()->setStretchLastSection(true);
    
    ui->tableWidgetStats->setEditTriggers(QAbstractItemView::NoEditTriggers);
    ui->tableWidgetStats->horizontalHeader()->setStretchLastSection(true);
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
    
    // Add to practice player combo box
    ui->comboBoxPracticePlayer->addItem(name);
    
    // Clear input fields
    ui->lineEditName->clear();
    ui->comboBoxPosition->setCurrentIndex(0);
    ui->spinBoxAge->setValue(20);
    
    // Show success message
    QMessageBox::information(this, "成功", QString("球員 %1 已新增！").arg(player.name));
}

void MainWindow::onStartPracticeClicked()
{
    if (ui->comboBoxPracticePlayer->count() == 0) {
        QMessageBox::warning(this, "警告", "請先新增球員！");
        return;
    }
    
    currentPlayerName = ui->comboBoxPracticePlayer->currentText();
    currentDistance = ui->spinBoxDistance->value();
    currentAttempts = 0;
    currentSuccessfulGoals = 0;
    practiceInProgress = true;
    
    // Start timer
    practiceTimer.start();
    
    // Update UI
    ui->pushButtonStartPractice->setEnabled(false);
    ui->pushButtonRecordGoal->setEnabled(true);
    ui->pushButtonRecordMiss->setEnabled(true);
    ui->pushButtonEndPractice->setEnabled(true);
    ui->comboBoxPracticePlayer->setEnabled(false);
    ui->spinBoxDistance->setEnabled(false);
    ui->spinBoxTotalAttempts->setEnabled(false);
    
    updatePracticeDisplay();
}

void MainWindow::onRecordGoalClicked()
{
    if (!practiceInProgress) {
        return;
    }
    
    currentSuccessfulGoals++;
    currentAttempts++;
    
    updatePracticeDisplay();
    checkAndAutoEndPractice();
}

void MainWindow::onRecordMissClicked()
{
    if (!practiceInProgress) {
        return;
    }
    
    currentAttempts++;
    
    updatePracticeDisplay();
    checkAndAutoEndPractice();
}

void MainWindow::onEndPracticeClicked()
{
    if (!practiceInProgress) {
        return;
    }
    
    // Stop timer and get elapsed time
    qint64 elapsed = 0;
    if (practiceTimer.isValid()) {
        elapsed = practiceTimer.elapsed();
    }
    
    // Save practice session
    PracticeSession session;
    session.distance = currentDistance;
    session.totalAttempts = currentAttempts;
    session.successfulGoals = currentSuccessfulGoals;
    session.timeSpent = elapsed;
    session.playerName = currentPlayerName;
    
    // Find player and add session
    for (int i = 0; i < players.size(); i++) {
        if (players[i].name == currentPlayerName) {
            players[i].practiceSessions.append(session);
            break;
        }
    }
    
    // Show summary
    double successRate = calculateSuccessRate(currentSuccessfulGoals, currentAttempts);
    QString summary = QString("練習完成！\n\n"
                             "球員: %1\n"
                             "距離: %2 碼\n"
                             "總嘗試: %3 次\n"
                             "成功進球: %4 次\n"
                             "成功率: %5%\n"
                             "花費時間: %6 秒")
                        .arg(currentPlayerName)
                        .arg(currentDistance)
                        .arg(currentAttempts)
                        .arg(currentSuccessfulGoals)
                        .arg(successRate, 0, 'f', 1)
                        .arg(convertToSeconds(elapsed), 0, 'f', 1);
    
    QMessageBox::information(this, "練習記錄", summary);
    
    // Reset UI
    practiceInProgress = false;
    ui->pushButtonStartPractice->setEnabled(true);
    ui->pushButtonRecordGoal->setEnabled(false);
    ui->pushButtonRecordMiss->setEnabled(false);
    ui->pushButtonEndPractice->setEnabled(false);
    ui->comboBoxPracticePlayer->setEnabled(true);
    ui->spinBoxDistance->setEnabled(true);
    ui->spinBoxTotalAttempts->setEnabled(true);
    ui->labelPracticeInfo->setText("尚未開始練習");
    
    // Update stats table
    updateStatsTable();
}

void MainWindow::onShowStatsClicked()
{
    updateStatsTable();
    QMessageBox::information(this, "提示", "統計數據已更新！");
}

void MainWindow::updatePracticeDisplay()
{
    if (!practiceInProgress || !practiceTimer.isValid()) {
        return;
    }
    
    int plannedAttempts = ui->spinBoxTotalAttempts->value();
    double successRate = calculateSuccessRate(currentSuccessfulGoals, currentAttempts);
    qint64 elapsed = practiceTimer.elapsed();
    
    QString info = QString("進行中 - %1\n距離: %2 碼 | 進度: %3/%4\n成功: %5 | 成功率: %6% | 時間: %7 秒")
                    .arg(currentPlayerName)
                    .arg(currentDistance)
                    .arg(currentAttempts)
                    .arg(plannedAttempts)
                    .arg(currentSuccessfulGoals)
                    .arg(successRate, 0, 'f', 1)
                    .arg(convertToSeconds(elapsed), 0, 'f', 1);
    
    ui->labelPracticeInfo->setText(info);
}

void MainWindow::updateStatsTable()
{
    ui->tableWidgetStats->setRowCount(0);
    
    for (const Player &player : players) {
        for (const PracticeSession &session : player.practiceSessions) {
            int row = ui->tableWidgetStats->rowCount();
            ui->tableWidgetStats->insertRow(row);
            
            double successRate = calculateSuccessRate(session.successfulGoals, session.totalAttempts);
            double timeInSeconds = convertToSeconds(session.timeSpent);
            
            ui->tableWidgetStats->setItem(row, 0, new QTableWidgetItem(player.name));
            ui->tableWidgetStats->setItem(row, 1, new QTableWidgetItem(QString::number(session.distance)));
            ui->tableWidgetStats->setItem(row, 2, new QTableWidgetItem(QString::number(session.totalAttempts)));
            ui->tableWidgetStats->setItem(row, 3, new QTableWidgetItem(QString::number(session.successfulGoals)));
            ui->tableWidgetStats->setItem(row, 4, new QTableWidgetItem(QString::number(successRate, 'f', 1)));
            ui->tableWidgetStats->setItem(row, 5, new QTableWidgetItem(QString::number(timeInSeconds, 'f', 1)));
        }
    }
}

void MainWindow::checkAndAutoEndPractice()
{
    int plannedAttempts = ui->spinBoxTotalAttempts->value();
    if (currentAttempts >= plannedAttempts) {
        QMessageBox::information(this, "提示", "已完成計劃的嘗試次數！");
        onEndPracticeClicked();
    }
}

double MainWindow::calculateSuccessRate(int successful, int total) const
{
    return total > 0 ? (static_cast<double>(successful) / total * 100.0) : 0.0;
}

double MainWindow::convertToSeconds(qint64 milliseconds) const
{
    return milliseconds / 1000.0;
}
