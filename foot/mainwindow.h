#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QString>
#include <QVector>
#include <QElapsedTimer>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

struct PracticeSession {
    int distance;           // Distance in yards
    int totalAttempts;      // Total number of attempts
    int successfulGoals;    // Number of successful goals
    qint64 timeSpent;       // Time spent in milliseconds
    QString playerName;     // Player who performed the practice
};

struct Player {
    QString name;
    QString position;
    int age;
    QVector<PracticeSession> practiceSessions;  // Practice history
};

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void onAddPlayerClicked();
    void onStartPracticeClicked();
    void onRecordGoalClicked();
    void onEndPracticeClicked();
    void onPlayerSelectionChanged();
    void onShowStatsClicked();

private:
    void updatePracticeDisplay();
    void updateStatsTable();
    QString calculatePlayerStats(const Player &player);
    
    Ui::MainWindow *ui;
    QVector<Player> players;
    QElapsedTimer practiceTimer;
    int currentAttempts;
    int currentSuccessfulGoals;
    int currentDistance;
    bool practiceInProgress;
    QString currentPlayerName;
};
#endif // MAINWINDOW_H
