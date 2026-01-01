#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include <QFileDialog>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonValue>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
    , currentAttempts(0)
    , currentSuccessfulGoals(0)
    , currentDistance(8)
    , practiceInProgress(false)
    , hasVideoAnalysisData(false)
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
    
    // Connect video analysis button
    connect(ui->pushButtonLoadVideoAnalysis, &QPushButton::clicked, this, &MainWindow::onLoadVideoAnalysisClicked);
    
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

void MainWindow::onLoadVideoAnalysisClicked()
{
    QString fileName = QFileDialog::getOpenFileName(this,
        tr("選擇視頻分析數據文件"), 
        QString(),
        tr("JSON Files (*.json);;All Files (*)"));
    
    if (fileName.isEmpty()) {
        return;
    }
    
    if (loadVideoAnalysisData(fileName)) {
        displayVideoAnalysisData();
        QMessageBox::information(this, "成功", "視頻分析數據已載入！");
    } else {
        QMessageBox::warning(this, "錯誤", "無法載入視頻分析數據文件！");
    }
}

bool MainWindow::loadVideoAnalysisData(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return false;
    }
    
    QByteArray jsonData = file.readAll();
    file.close();
    
    QJsonDocument doc = QJsonDocument::fromJson(jsonData);
    if (doc.isNull() || !doc.isObject()) {
        return false;
    }
    
    QJsonObject root = doc.object();
    if (!root.contains("metadata")) {
        return false;
    }
    
    QJsonObject metadata = root["metadata"].toObject();
    
    // Validate that all required fields exist
    QStringList requiredFields = {
        "total_frames", "team_1_ball_control_percent", "team_2_ball_control_percent",
        "team_1_attack_percent", "team_2_attack_percent"
    };
    
    for (const QString &field : requiredFields) {
        if (!metadata.contains(field)) {
            return false;
        }
    }
    
    // Extract data with default values as fallback
    videoAnalysisData.totalFrames = metadata.value("total_frames").toInt(0);
    videoAnalysisData.team1PossessionPercent = metadata.value("team_1_ball_control_percent").toDouble(0.0);
    videoAnalysisData.team2PossessionPercent = metadata.value("team_2_ball_control_percent").toDouble(0.0);
    videoAnalysisData.team1AttackPercent = metadata.value("team_1_attack_percent").toDouble(0.0);
    videoAnalysisData.team2AttackPercent = metadata.value("team_2_attack_percent").toDouble(0.0);
    videoAnalysisData.team1AttackFrames = metadata.value("team_1_attack_frames").toInt(0);
    videoAnalysisData.team2AttackFrames = metadata.value("team_2_attack_frames").toInt(0);
    videoAnalysisData.team1TotalDistanceKm = metadata.value("team_1_total_distance_km").toDouble(0.0);
    videoAnalysisData.team2TotalDistanceKm = metadata.value("team_2_total_distance_km").toDouble(0.0);
    videoAnalysisData.team1AvgDistancePerPlayerM = metadata.value("team_1_avg_distance_per_player_m").toDouble(0.0);
    videoAnalysisData.team2AvgDistancePerPlayerM = metadata.value("team_2_avg_distance_per_player_m").toDouble(0.0);
    videoAnalysisData.team1AvgSpeedKmh = metadata.value("team_1_avg_speed_kmh").toDouble(0.0);
    videoAnalysisData.team2AvgSpeedKmh = metadata.value("team_2_avg_speed_kmh").toDouble(0.0);
    videoAnalysisData.team1PlayerCount = metadata.value("team_1_player_count").toInt(0);
    videoAnalysisData.team2PlayerCount = metadata.value("team_2_player_count").toInt(0);
    videoAnalysisData.dataFilePath = filePath;
    
    // Extract possession frames (may not be present in older exports)
    videoAnalysisData.team1PossessionFrames = metadata.value("team_1_frames").toInt(0);
    videoAnalysisData.team2PossessionFrames = metadata.value("team_2_frames").toInt(0);
    
    hasVideoAnalysisData = true;
    return true;
}

void MainWindow::displayVideoAnalysisData()
{
    if (!hasVideoAnalysisData) {
        return;
    }
    
    // Update labels with possession data
    ui->labelTeam1Possession->setText(QString("隊伍 1 持球時間: %1%")
        .arg(videoAnalysisData.team1PossessionPercent, 0, 'f', 2));
    ui->labelTeam2Possession->setText(QString("隊伍 2 持球時間: %1%")
        .arg(videoAnalysisData.team2PossessionPercent, 0, 'f', 2));
    
    // Update labels with attack data
    ui->labelTeam1Attack->setText(QString("隊伍 1 進攻時間: %1%")
        .arg(videoAnalysisData.team1AttackPercent, 0, 'f', 2));
    ui->labelTeam2Attack->setText(QString("隊伍 2 進攻時間: %1%")
        .arg(videoAnalysisData.team2AttackPercent, 0, 'f', 2));
    
    // Update labels with distance data
    ui->labelTeam1Distance->setText(QString("隊伍 1 總距離: %1 公里")
        .arg(videoAnalysisData.team1TotalDistanceKm, 0, 'f', 2));
    ui->labelTeam2Distance->setText(QString("隊伍 2 總距離: %1 公里")
        .arg(videoAnalysisData.team2TotalDistanceKm, 0, 'f', 2));
    
    // Update labels with speed data
    ui->labelTeam1Speed->setText(QString("隊伍 1 平均速度: %1 公里/小時")
        .arg(videoAnalysisData.team1AvgSpeedKmh, 0, 'f', 2));
    ui->labelTeam2Speed->setText(QString("隊伍 2 平均速度: %1 公里/小時")
        .arg(videoAnalysisData.team2AvgSpeedKmh, 0, 'f', 2));
    
    // Update summary info
    QString summaryText = QString("總幀數: %1\n"
                                  "隊伍 1 持球幀數: %2 | 進攻幀數: %3\n"
                                  "隊伍 2 持球幀數: %4 | 進攻幀數: %5\n"
                                  "隊伍 1 球員數: %6 | 平均每人距離: %7 公尺\n"
                                  "隊伍 2 球員數: %8 | 平均每人距離: %9 公尺")
        .arg(videoAnalysisData.totalFrames)
        .arg(videoAnalysisData.team1PossessionFrames)
        .arg(videoAnalysisData.team1AttackFrames)
        .arg(videoAnalysisData.team2PossessionFrames)
        .arg(videoAnalysisData.team2AttackFrames)
        .arg(videoAnalysisData.team1PlayerCount)
        .arg(videoAnalysisData.team1AvgDistancePerPlayerM, 0, 'f', 1)
        .arg(videoAnalysisData.team2PlayerCount)
        .arg(videoAnalysisData.team2AvgDistancePerPlayerM, 0, 'f', 1);
    
    ui->labelVideoAnalysisSummary->setText(summaryText);
}
