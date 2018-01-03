Private Sub btnMeas_Click()

    env.flgstop = False
    Call statusbar.text(SB_STATE, "")
    
    Call putdata.SetRefCell(Cells(ActiveCell.row, 1))
    
    Dim sTime, eTime
    sTime = Now
    Call statusbar.text(SB_START, "Start " & Right("0" & Hour(sTime), 2) & ":" & Right("0" & Minute(sTime), 2))
    
    DoEvents
    If env.flgstop Then GoTo cancel_end
    
    ' List Measuring Condition
    Dim cond As clsCondition
    Set cond = New clsCondition
    
    Dim start, step, down As Integer, up As Integer
    
    ' Check COM port
    Me.txtCom.BackColor = vbCyan
    If Not ecMic.isAvailable(CInt(Me.txtCom)) Then
        MsgBox ("COM" & Me.txtCom & " が開けません")
        Me.txtCom.BackColor = vbWindowBackground
        GoTo cancel_end
    End If
    
    If Not ecMic.isMdioAvailable(CInt(Me.txtCom), 0, 1) Then
        MsgBox ("MDIO deviceが応答しません")
        Me.txtCom.BackColor = vbWindowBackground
        GoTo cancel_end
    End If
    Me.txtCom.BackColor = vbWindowBackground

    env.com = CInt(Me.txtCom)

    DoEvents
    If env.flgstop Then GoTo cancel_end
    
    ' password required for first time
    cfpmic.SendPasswordCfp8 (CInt(Me.txtCom))
    Debug.Assert (ecMic.LastState = 0)
    
    Dim serial As String
    serial = cfpmic.GetSN(CInt(Me.txtCom), 0, 1)
    
    Dim opm As Object
    Set opm = New clsPowerMeter
    opm.Init (Me.txtVisaOpticalPowerMeter)
    opm.slot = 1
    Set env.opm = opm
    
    Dim optatt As Object
    Set optatt = New clsOptAtt
    optatt.Init (Me.txtVisaOptAtt)
    Set env.att = optatt
    
    If Me.chkPsu Then
        Dim psu As Object
        Set psu = New clsPowerSupply
        psu.Init (Me.txtVisaPowerSupply)
        If Not psu.Initialized Then GoTo cancel_end
    End If
    
    Dim wavelength(7) As Integer
    wavelength(0) = 1274
    wavelength(1) = 1278
    wavelength(2) = 1282
    wavelength(3) = 1287
    wavelength(4) = 1296
    wavelength(5) = 1300
    wavelength(6) = 1305
    wavelength(7) = 1309
    
    Dim items() As String
    Dim item As String
    Dim vals
    Dim val
    Dim i
    Dim att As Double
    
    env.webapi = Me.chkWebApi
    env.phyad = 0
    env.devad = 1
    env.devad_south = 21
            
restart_lanes:
    
    env.lane = Me.cmbLane.ListIndex
    
    Call opm.SetWavelength(wavelength(env.lane))
    
    DoEvents
    If env.flgstop Then GoTo cancel_end
    
    ' Start Measurement Loop
    cond.First
    Do While cond.GoNext
        
        Call statusbar.text(SB_POINT, cond.current & "/" & cond.Count)
        
        Dim heads(1) As String
        heads(0) = Me.txtTitle & " " & Me.cmbLane.value & " " & cond.ToString
        heads(1) = guid.CreateGuid()
        
        Call putdata.SetHeaders(heads)
        postdata.Enable = Me.chkWebApi
        Call postdata.SetHeader(Me.txtTitle, cond.ToString, serial, env.lane, heads(1))
        
        Dim k
        For Each k In cond.Keys
            If Not cond.value(CStr(k)) = "Nothing" Then
                Call putdata.AddEntry(CStr(k), cond.value(CStr(k)))
            End If
        Next
                
        DoEvents
        If env.flgstop Then GoTo cancel_end
        
        Call putdata.AddEntry("S/N", serial)
        Call putdata.AddEntry("Lane", env.lane)
               
        DoEvents
        If env.flgstop Then GoTo cancel_end
        
        If Me.chkPsu Then
            val = psu.GetVoltage()
            Call putdata.AddEntry("Vcc_PSU", val)
            Call postdata.AddEntry("Vcc_PSU", val)
            val = psu.GetCurrent()
            Call putdata.AddEntry("Icc_PSU", val)
            Call postdata.AddEntry("Icc_PSU", val)
            
            DoEvents
            If env.flgstop Then GoTo cancel_end
        End If
        
        putdata.RefCellActivate
        
        DoEvents
        If env.flgstop Then GoTo cancel_end
        
        Call cfp8meas.MonModuleTemp(env)
        
        putdata.RefCellActivate
        
        DoEvents
        If env.flgstop Then GoTo cancel_end
        
        ' Error Distribution
        If Me.chkBER Then
            Dim orig_att As Double
            orig_att = optatt.GetAtt()
        
            Call cfp8meas.ErrorDistribution(env, Me.chkAtt, CDbl(Me.txtAttStart), CDbl(Me.txtAttStop), CDbl(Me.txtAttStep), CLng(Me.txtBerInterval))
                
        End If
                
        ReDim items(5)
        ReDim vals(5)
                        
        ' Optical Power measurement without BER measure
        If Not Me.chkBER Then
            ' Lane Select
            Call cfpmic.ContTxDis(env.com, env.phyad, env.devad, &HFF Xor 2 ^ env.lane)
            Wait.Wait (2)

            items(0) = "OpticalPower"
            items(1) = "OpticalATT"
            items(2) = "RxPowerADC"
            items(3) = "TxPowerADC"
            items(4) = "RxPowerMon"
            items(5) = "TxPowerMon"
            Call putdata.AddItems(items)

            att = CDbl(Me.txtAttStart)
            Debug.Assert CDbl(Me.txtAttStep) > 0
            Debug.Assert CDbl(Me.txtAttStop) > CDbl(Me.txtAttStart)
            Do
                DoEvents
                If env.flgstop Then GoTo cancel_end

                If Me.chkAtt Then
                    Call optatt.SetAtt(att)
                    Wait.Wait (1)
                End If

                vals(0) = opm.GetPower
                vals(1) = optatt.GetAtt
                vals(2) = cfpmic.GetAdcRxPowerCfp8(env.com, env.lane)
                vals(3) = cfpmic.GetAdcTxPowerCfp8(env.com, env.lane)
                vals(4) = cfpmic.GetMonRxPowerdBm(env.com, env.phyad, env.devad, env.lane)
                vals(5) = cfpmic.GetMonTxPowerdBm(env.com, env.phyad, env.devad, env.lane)
                Call putdata.AddValues(vals)
                Call postdata.AddEntries(items, vals)

                att = att + CDbl(Me.txtAttStep)
            Loop While (att <= CDbl(Me.txtAttStop) And Me.chkAtt)

            putdata.RefCellActivate

            DoEvents
            If env.flgstop Then GoTo cancel_end
        End If
        
        If Me.chkRxSlope Then
            For att = 4 To 14 Step 5
                Call optatt.SetAtt(att)
                Wait.Wait (1)
                
                Call cfp8meas.MonOptPower(env, "_ATT" & att)
            Next
        End If
        
        putdata.RefCellActivate
        
        DoEvents
        If env.flgstop Then GoTo cancel_end
                           
        If Me.chkAtt Then
            Call optatt.SetAtt(orig_att)
        End If
        
        If Me.chkTxSlope Then
        
            For i = 0 To 7
                item = "TxPowerADC_L" & i
                val = cfpmic.GetAdcTxPowerCfp8(env.com, CInt(i))
                Call putdata.AddEntry(item, val)
                Call postdata.AddEntry(item, val)
            Next

            Dim orig_ldbias As Long
            orig_ldbias = GetLdBiasCfp8(env.com, env.lane)
            
            Call cfpmic.SetLdBiasCfp8(env.com, env.lane, 5000)
            Wait.Wait (1)
            
            Call cfp8meas.MonOptPower(env, "_LDbias5000")
            
            Call cfpmic.SetLdBiasCfp8(env.com, env.lane, orig_ldbias)
        End If
        
        putdata.RefCellActivate
        
        DoEvents
        If env.flgstop Then GoTo cancel_end
        
        ' Lane Cancel
        Call cfpmic.ContTxDis(env.com, env.phyad, env.devad, 0)
        Wait.Wait (1)
            
        If Me.chkTxSlope Then
            
            Call cfp8meas.MonOptPower(env, "_ALL_ON")
            
            putdata.RefCellActivate
            
            DoEvents
            If env.flgstop Then GoTo cancel_end

            ' All Lane Off
            Call cfpmic.ContTxDis(env.com, env.phyad, env.devad, &HFF)
            Wait.Wait (2)
            
            Call cfp8meas.MonOptPower(env, "_ALL_OFF")
            
            ' Lane Cancel
            Call cfpmic.ContTxDis(env.com, env.phyad, env.devad, 0)
            Wait.Wait (1)
            
            putdata.RefCellActivate
            
            DoEvents
            If env.flgstop Then GoTo cancel_end
        
        End If
        
        If Me.chkBER Then
                
            ' SNR4
            vals = cfpmic.GetApiPamReadLevelSnr(env.com, env.lane)
            'Call putdata.AddItem("SNR")
            For i = 0 To 3
                Call putdata.AddEntry("SNR" & i, vals(i))
                Call postdata.AddEntry("SNR" & i, vals(i))
            Next
            
            putdata.RefCellActivate
            
            DoEvents
            If env.flgstop Then GoTo cancel_end
            
            ' PGA
            vals = cfpmic.GetApiPamReadCpga(env.com, env.lane)
            Call putdata.AddEntry("PGA", vals)
            Call postdata.AddEntry("PGA", vals)
            
            DoEvents
            If env.flgstop Then GoTo cancel_end
        
            ' LDD Peak
            vals = cfpmic.GetAdcPeakCfp8(env.com, env.lane)
            Call putdata.AddEntry("Peak", vals)
            Call postdata.AddEntry("Peak", vals)
            
            DoEvents
            If env.flgstop Then GoTo cancel_end
            
        End If
        
        putdata.RefCellActivate
        
        DoEvents
        If env.flgstop Then GoTo cancel_end
        
    Loop
    
    Call statusbar.text(SB_STATE, "")
    
    If Me.chkAllLane Then
        If Me.cmbLane.ListIndex < Me.cmbLane.ListCount - 1 Then
            Me.cmbLane.ListIndex = Me.cmbLane.ListIndex + 1
            GoTo restart_lanes
        Else
            Me.cmbLane.ListIndex = 0
        End If
    End If
    
    Call statusbar.text(SB_STATE, "complete. " & Format(Now - sTime, "hh:mm:ss"))
    Exit Sub
    
cancel_end:

   If Me.chkAllLane Then Me.cmbLane.ListIndex = 0
   Call statusbar.text(SB_STATE, "canceled. " & Format(Now - sTime, "hh:mm:ss"))
End Sub

